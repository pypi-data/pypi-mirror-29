# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import numpy as np
import tensorflow as tf
import polyaxon_lib as plx

from tensorflow.python.estimator.inputs.numpy_io import numpy_input_fn

from polyaxon_schemas.losses import AbsoluteDifferenceConfig
from polyaxon_schemas.optimizers import SGDConfig

tf.logging.set_verbosity(tf.logging.INFO)

# Data
X = np.asarray([[0., 0.], [0., 1.], [1., 0.], [1., 1.]], dtype=np.float32)
y = np.asarray([[0], [1], [1], [0]], dtype=np.float32)


def graph_fn(mode, features):
    x = plx.layers.Dense(units=32, activation='tanh')(features['X'])
    return plx.layers.Dense(units=1, activation='sigmoid')(x)


def model_fn(features, labels, mode):
    model = plx.models.Regressor(
        mode,
        graph_fn=graph_fn,
        loss=AbsoluteDifferenceConfig(),
        optimizer=SGDConfig(learning_rate=0.5, decay_type='exponential_decay', decay_steps=10),
        summaries='all',
        name='xor')
    return model(features, labels)


estimator = plx.estimators.Estimator(model_fn=model_fn, model_dir="/tmp/polyaxon_logs/xor")


def input_fn(num_epochs=1):
    return numpy_input_fn({'X': X}, y,
                          shuffle=False,
                          num_epochs=num_epochs,
                          batch_size=len(X))

estimator.train(input_fn(10000))


print([x['results'] for x in estimator.predict(input_fn())])
print(y)
