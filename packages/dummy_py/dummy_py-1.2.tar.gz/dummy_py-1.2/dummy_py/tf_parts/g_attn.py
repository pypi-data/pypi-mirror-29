from typing import Union, Iterable, TYPE_CHECKING

import numpy as np
import tensorflow as tf
from tensorflow.contrib.layers import batch_norm

__all__ = [
    'sub_layer',
    'multi_head_attention',
    'encoder',
    'decoder',
]

if TYPE_CHECKING:
    tf_input = Union[tf.Tensor, np.ndarray]
    var_scope_or_name = Union[tf.VariableScope, str]


class NameScope(tf.name_scope):
    def __init__(self, name, default_name=None, values=None):
        super().__init__(name,
                         default_name='g_attn_{}'.format(default_name),
                         values=[_ for _ in values if _ is not None])

    def __enter__(self):
        self._cur_name = super().__enter__()  # type: str
        return self

    @property
    def scope_name(self):
        return self._cur_name

    def var_scope(self, scope_or_name: 'var_scope_or_name' = None, **kwargs):
        if scope_or_name is None:
            scope_or_name = self._cur_name.strip('/')
        return tf.variable_scope(scope_or_name, **kwargs)


def non_or(v, ctor):
    if v is not None:
        return v
    if callable(ctor):
        return ctor()
    return ctor


def normalization(x, name=None):
    with NameScope(name, 'norm', [x]):
        return x / tf.sqrt(tf.reduce_sum(tf.square(x), axis=-1, keep_dims=True))


def sub_layer(fn, x, *other_inputs, name=None, extra=None):
    """
    :param fn: sub layer body
    :param x: input x
    :param other_inputs: other input, not used as residual
    :param name: operator name
    :param extra: extra param for fn
    :return: batch_norm(x + fn(x))
    """
    with NameScope(name, 'sl', [x, *other_inputs]) as scope:
        after_residual = x + fn(x, *other_inputs, **non_or(extra, dict))
        with scope.var_scope():
            return batch_norm(after_residual)


def multi_head_attention(q: 'tf_input',
                         k: 'tf_input',
                         v: 'tf_input',
                         d_model: 'int',
                         n_head: 'int',
                         attn_mask: 'tf_input' = None,
                         name: 'str' = None,
                         dtype: 'tf.DType' = tf.float32):
    """
    :param q: query    [B, Tq,  Dq]
    :param k: key      [B, Tkv, Dk]
    :param v: value    [B, Tkv, Dv]
    :param d_model: see paper
    :param n_head: see paper
    :param attn_mask: attention mask, [B, Tq, Dq] (support broadcast), for avoid decoder forward depends
    :param name: operator name
    :param dtype: data dtype, default float32
    :return: see paper
    """
    with NameScope(name, 'mha', [q, k, v]) as scope:
        qk_same = q is k
        kv_same = k is v
        q = tf.convert_to_tensor(q, dtype)
        if qk_same:
            k = q
        else:
            k = tf.convert_to_tensor(k, dtype)
        if kv_same:
            v = k
        else:
            v = tf.convert_to_tensor(v, dtype)
        if attn_mask is not None:
            attn_mask = tf.convert_to_tensor(attn_mask, dtype)

        def control_dependencies():
            q_shape = tf.shape(q)
            yield tf.assert_equal(tf.shape(q_shape), [3], message="query as 3-D tensor")

            if not qk_same:
                k_shape = tf.shape(k)
                yield tf.assert_equal(tf.shape(k_shape), [3], message="key as 3-D tensor")
                yield tf.assert_equal(q_shape[0], k_shape[0], message="query & key has same batch size (dim[0])")

                if not kv_same:
                    v_shape = tf.shape(v)
                    yield tf.assert_equal(tf.shape(v_shape), [3], message="value as 3-D tensor")
                    yield tf.assert_equal(k_shape[:-1], v_shape[:-1],
                                          message="key & value has same batch size(dim[0]) and seq-len(dim[1])")

        with tf.control_dependencies(list(control_dependencies())):
            with scope.var_scope():
                q_dense = tf.layers.dense(q, d_model * n_head, use_bias=False, name='q')
                k_dense = tf.layers.dense(k, d_model * n_head, use_bias=False, name='k')
                v_dense = tf.layers.dense(v, d_model * n_head, use_bias=False, name='v')

            q_n_head = tf.concat(tf.split(q_dense, n_head, axis=-1), axis=0)
            k_n_head = tf.concat(tf.split(k_dense, n_head, axis=-1), axis=0)
            v_n_head = tf.concat(tf.split(v_dense, n_head, axis=-1), axis=0)

            qk_n_head = tf.matmul(q_n_head, k_n_head, transpose_b=True)  # [B * n_head, Tq, Tkv]
            attn_n_head = tf.nn.softmax(qk_n_head / (d_model ** 0.5))
            if attn_mask is not None:
                attn_n_head = normalization(attn_n_head * attn_mask)
            attn_v_n_head = tf.matmul(attn_n_head, v_n_head)  # [B * n_head, Tq, d_model]
            attn_v = tf.concat(tf.split(attn_v_n_head, n_head, axis=0), axis=-1)
            with scope.var_scope():
                return tf.layers.dense(attn_v, d_model, use_bias=False, name='o')


def feed_forward(x: 'tf.Tensor',
                 num_units: 'int' = None,
                 name: 'str' = None, dtype: 'tf.DType' = None):
    """
    :param x: input
    :param num_units: output size
    :param name: operator name
    :param dtype: data type, default to input dtype
    :return: max(0, x*w0+b0)*w1 + b1
    """
    with NameScope(name, 'ff', [x]) as scope:
        x = tf.convert_to_tensor(x, dtype)
        if num_units is None:
            num_units = tf.shape(x)[-1]
        with scope.var_scope():
            return tf.layers.dense(tf.layers.dense(x, num_units, activation=tf.nn.relu), num_units)


def encoder(x: 'tf_input',
            pos_encoding: 'tf_input',
            n_head: 'int',
            n_stack: 'int',
            d_model: 'int',
            context: 'Iterable[tf_input]' = None,
            name: 'str' = None,
            dtype: 'tf.DType' = tf.float32):
    """
    encoder, input size and pos encoding size must be d_model

    :param x: input (eg. word embedding), [Batch, TimeStep, d_model]
    :param pos_encoding: pos encoding, could be learned or sin/cos curve, same shape as input(support broadcast)
    :param n_head: see paper
    :param n_stack: see paper
    :param d_model: see paper
    :param context: previous step data, from return value
    :param name: operator name
    :param dtype: data type, default float32
    :return: (encoder result, current context)
    """
    with NameScope(name, 'encoder', [x, pos_encoding] + non_or(context, list)):
        x = tf.convert_to_tensor(x, dtype)
        pos_encoding = tf.convert_to_tensor(pos_encoding, dtype)

        def control_dependencies():
            x_shape = tf.shape(x)
            x_dims = tf.shape(x_shape)
            yield tf.assert_equal(x_dims, [3])
            yield tf.assert_equal(x_shape[2], d_model)

            pe_shape = tf.shape(pos_encoding)
            pe_dims = tf.shape(pe_shape)
            yield tf.assert_equal(pe_dims, [3])

            yield tf.Assert(tf.logical_or(tf.equal(pe_shape[0], x_shape[0]),
                                          tf.equal(pe_shape[0], 1)),
                            [pe_dims])
            yield tf.Assert(tf.logical_or(tf.equal(pe_shape[1], x_shape[1]),
                                          tf.equal(pe_shape[1], 1)),
                            [pe_dims])
            yield tf.Assert(tf.logical_or(tf.equal(pe_shape[2], x_shape[2]),
                                          tf.equal(pe_shape[2], 1)),
                            [pe_dims])

        with tf.control_dependencies(list(control_dependencies())):
            v = x + pos_encoding
            v_list = []
            if context is not None:
                context = [tf.convert_to_tensor(_, dtype) for _ in context]
                assert len(context) == n_stack
            for i in range(n_stack):
                v_list.append(v)
                self_attn_q = v
                self_attn_kv = v if context is None else tf.concat((v, context[i]), axis=-1)
                v = sub_layer(multi_head_attention, self_attn_q, self_attn_kv, self_attn_kv, d_model, n_head,
                              name='stack_{}_sa'.format(i),
                              extra={'dtype': dtype})
                v = sub_layer(feed_forward, v, d_model, name='stack_{}_ff'.format(i), extra={'dtype': dtype})
    return v, v_list


def decoder(x: 'tf_input',
            pos_encoding: 'tf_input',
            encoder_output: 'tf_input',
            n_head: 'int',
            n_stack: 'int',
            d_model: 'int',
            attn_mask: 'tf_input' = None,
            context: 'Iterable[tf_input]' = None,
            name: 'str' = None,
            dtype: 'tf.DType' = tf.float32):
    """
    :param x: input (eg. word embedding), [Batch, TimeStep, d_model]
    :param pos_encoding: pos encoding, could be learned or sin/cos curve, same shape as input(support broadcast)
    :param encoder_output: encoder output, [Batch, EncoderTimeStep, EncoderDModel]
    :param n_head: see paper
    :param n_stack: see paper
    :param d_model: see paper
    :param context: previous step data, from return value
    :param attn_mask: attn mask for self attention, see multi_head_attention method
    :param name: operator name
    :param dtype: data type, default float32
    :return: (decoder result, current context)
    """
    with NameScope(name, 'decoder', [x, pos_encoding, attn_mask] + non_or(context, list)):
        x = tf.convert_to_tensor(x, dtype)
        pos_encoding = tf.convert_to_tensor(pos_encoding, dtype)
        encoder_output = tf.convert_to_tensor(encoder_output, dtype)

        def control_dependencies():
            x_shape = tf.shape(x)
            x_dims = tf.shape(x_shape)
            yield tf.assert_equal(x_dims, [3])
            yield tf.assert_equal(x_shape[2], d_model)

            pe_shape = tf.shape(pos_encoding)
            pe_dims = tf.shape(pe_shape)
            yield tf.assert_equal(pe_dims, [3])

            yield tf.Assert(tf.logical_or(tf.equal(pe_shape[0], x_shape[0]),
                                          tf.equal(pe_shape[0], 1)),
                            [pe_dims])
            yield tf.Assert(tf.logical_or(tf.equal(pe_shape[1], x_shape[1]),
                                          tf.equal(pe_shape[1], 1)),
                            [pe_dims])
            yield tf.Assert(tf.logical_or(tf.equal(pe_shape[2], x_shape[2]),
                                          tf.equal(pe_shape[2], 1)),
                            [pe_dims])

            eo_shape = tf.shape(encoder_output)
            eo_dims = tf.shape(eo_shape)
            yield tf.equal(eo_dims, 3)
            yield tf.equal(eo_shape[0], x_shape[0])

        if context is not None:
            context = [tf.convert_to_tensor(_, dtype) for _ in context]
            assert len(context) == n_stack
        with tf.control_dependencies(list(control_dependencies())):
            v = x + pos_encoding
            v_list = []
            for i in range(n_stack):
                v_list.append(v)
                self_attn_q = v
                self_attn_kv = v if context is None else tf.concat((v, context[i]), axis=-1)
                v = sub_layer(multi_head_attention, self_attn_q, self_attn_kv, self_attn_kv, d_model, n_head,
                              name='stack_{}_sa'.format(i),
                              extra={'attn_mask': attn_mask,
                                     'dtype': dtype})
                v = sub_layer(multi_head_attention, v, encoder_output, encoder_output, d_model, n_head,
                              name='stack_{}_a'.format(i),
                              extra={'dtype': dtype})
                v = sub_layer(feed_forward, v, d_model, name='stack_{}_ff'.format(i), extra={'dtype': dtype})
    return v, v_list
