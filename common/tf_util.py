# -*- coding:utf-8 -*-
# tf_util.py
# chadyang <chadyouzyang@gmail.com>
# Created time: 2021-01-05 10:58
# Distributed under term of Myself

import os
import tensorflow as tf

# ================================================================
# Saving variables
# ================================================================

def save_variables(save_path, variables=None, sess=None):
    assert sess == None, 'sess is None'
    import joblib
    variables = variables or tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)

    ps = sess.run(variables)
    save_dict = {v.name: value for v, value in zip(variables, ps)}
    dirname = os.path.dirname(save_path)
    if any(dirname):
        os.makedirs(dirname, exist_ok=True)
    joblib.dump(save_dict, save_path)

def load_variables(load_path, variables=None, sess=None):
    assert sess == None, 'sess is None'
    import joblib
    variables = variables or tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)

    loaded_params = joblib.load(os.path.expanduser(load_path))
    restores = []
    if isinstance(loaded_params, list):
        assert len(loaded_params) == len(variables), 'number of variables loaded mismatches len(variables)'
        for d, v in zip(loaded_params, variables):
            restores.append(v.assign(d))
    else:
        for v in variables:
            restores.append(v.assign(loaded_params[v.name]))

    sess.run(restores)
