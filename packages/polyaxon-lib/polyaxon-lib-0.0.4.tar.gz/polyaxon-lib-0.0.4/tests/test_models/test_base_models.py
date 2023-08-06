# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
from polyaxon_schemas.losses import LogLossConfig
from polyaxon_schemas.optimizers import AdadeltaConfig

import polyaxon_lib as plx

from tensorflow.python.training import training
from tensorflow.python.platform import test

from polyaxon_lib.estimators.estimator_spec import EstimatorSpec
from polyaxon_lib.models import BaseModel
from polyaxon_lib.libs.utils import get_tracked


class TestBaseModel(test.TestCase):
    @staticmethod
    def get_dummy_graph_fn():
        def graph_fn(mode, features):
            x = plx.layers.Dense(units=1, activation='relu')(features['x'])
            x = plx.layers.Dense(units=1, activation='relu')(x)
            return x

        return graph_fn

    def test_build_no_summaries(self):
        x = {'x': tf.placeholder(tf.float32, [2, 89])}
        y = tf.constant([[1], [1]])

        model = BaseModel(plx.Modes.TRAIN,
                          graph_fn=self.get_dummy_graph_fn(),
                          loss=LogLossConfig(),
                          optimizer=AdadeltaConfig(),
                          model_type=BaseModel.Types.CLASSIFIER,
                          metrics=[],
                          summaries=[],
                          name='test')

        model(x, y, None, None)

        # Only activations are created
        summaries_by_names = get_tracked(collection=tf.GraphKeys.SUMMARIES_BY_NAMES)
        assert summaries_by_names == {}

    def test_build_activation_summaries(self):
        x = {'x': tf.placeholder(tf.float32, [2, 89])}
        y = tf.constant([[1], [1]])

        model = BaseModel(plx.Modes.TRAIN,
                          graph_fn=self.get_dummy_graph_fn(),
                          loss=LogLossConfig(),
                          optimizer=AdadeltaConfig(),
                          model_type=BaseModel.Types.CLASSIFIER,
                          metrics=[],
                          summaries=['activations'],
                          name='test')

        model(x, y, None, None)

        # Only activations are created
        summaries_by_names = get_tracked(collection=tf.GraphKeys.SUMMARIES_BY_NAMES)
        for s_name in summaries_by_names.keys():
            assert 'Activation' in s_name

    def test_build_loss_summaries(self):
        x = {'x': tf.placeholder(tf.float32, [2, 89])}
        y = tf.constant([[1], [1]])

        model = BaseModel(plx.Modes.TRAIN, graph_fn=self.get_dummy_graph_fn(),
                          loss=LogLossConfig(),
                          optimizer=AdadeltaConfig(),
                          model_type=BaseModel.Types.CLASSIFIER, metrics=[],
                          summaries=['loss'], name='test')

        model(x, y, None, None)

        # Only loss are created
        summaries_by_names = get_tracked(collection=tf.GraphKeys.SUMMARIES_BY_NAMES)
        for s_name in summaries_by_names.keys():
            assert 'Loss' in s_name

    def test_build_gradients_summaries(self):
        x = {'x': tf.placeholder(tf.float32, [2, 89])}
        y = tf.constant([[1], [1]])

        model = BaseModel(plx.Modes.TRAIN,
                          graph_fn=self.get_dummy_graph_fn(),
                          loss=LogLossConfig(),
                          optimizer=AdadeltaConfig(),
                          model_type=BaseModel.Types.CLASSIFIER,
                          metrics=[],
                          summaries=['gradients'],
                          name='test')

        model(x, y, None, None)

        # Only gradients are created
        summaries_by_names = get_tracked(collection=tf.GraphKeys.SUMMARIES_BY_NAMES)
        for s_name in summaries_by_names.keys():
            assert 'Gradient' in s_name

    def test_build_variables_summaries(self):
        x = {'x': tf.placeholder(tf.float32, [2, 89])}
        y = tf.constant([[1], [1]])

        model = BaseModel(plx.Modes.TRAIN,
                          graph_fn=self.get_dummy_graph_fn(),
                          loss=LogLossConfig(),
                          optimizer=AdadeltaConfig(),
                          model_type=BaseModel.Types.CLASSIFIER,
                          metrics=[],
                          summaries=['variables'],
                          name='test')

        model(x, y, None, None)

        # Only var are created
        variable_names = {var.op.name for var in tf.trainable_variables()}
        summaries_names = set(get_tracked(collection=tf.GraphKeys.SUMMARIES_BY_NAMES).keys())
        assert variable_names == summaries_names

    def test_build_learning_rate_summaries(self):
        training.create_global_step()
        x = {'x': tf.placeholder(tf.float32, [2, 89])}
        y = tf.constant([[1], [1]])

        model = BaseModel(plx.Modes.TRAIN, graph_fn=self.get_dummy_graph_fn(),
                          loss=LogLossConfig(),
                          optimizer=AdadeltaConfig(decay_type='exponential_decay'),
                          model_type=BaseModel.Types.CLASSIFIER, metrics=[],
                          summaries=['learning_rate'],
                          name='test')

        model(x, y, None, None)

        # Only var are created
        summaries_names = list(get_tracked(collection=tf.GraphKeys.SUMMARIES_BY_NAMES).keys())
        assert len(summaries_names) == 1
        assert summaries_names[0] == 'learning_rate'

    def test_does_not_build_learning_rate_summaries_if_no_decay(self):
        x = {'x': tf.placeholder(tf.float32, [2, 89])}
        y = tf.constant([[1], [1]])

        model = BaseModel(plx.Modes.TRAIN,
                          graph_fn=self.get_dummy_graph_fn(),
                          loss=LogLossConfig(),
                          optimizer=AdadeltaConfig(),
                          model_type=BaseModel.Types.CLASSIFIER,
                          metrics=[],
                          summaries=['learning_rate'],
                          name='test')

        model(x, y, None, None)

        # Only var are created
        summaries_names = list(get_tracked(collection=tf.GraphKeys.SUMMARIES_BY_NAMES).keys())
        assert len(summaries_names) == 0

    def test_build_all_summaries(self):
        training.create_global_step()
        x = {'x': tf.placeholder(tf.float32, [2, 89])}
        y = tf.constant([[1], [1]])

        model = BaseModel(plx.Modes.TRAIN, graph_fn=self.get_dummy_graph_fn(),
                          loss=LogLossConfig(),
                          optimizer=AdadeltaConfig(decay_type='exponential_decay'),
                          model_type=BaseModel.Types.CLASSIFIER,
                          metrics=[],
                          summaries='all',
                          name='test')

        model(x, y, None, None)

        # Only var are created
        learning_rate_summaries = 0
        activations_summaries = 0
        gradients_summaries = 0
        loss_summaries = 0

        for s_name in get_tracked(collection=tf.GraphKeys.SUMMARIES_BY_NAMES).keys():
            if 'learning_rate' in s_name:
                learning_rate_summaries += 1
            elif 'Activation' in s_name:
                activations_summaries += 1
            elif 'Loss' in s_name:
                loss_summaries += 1
            elif 'Gradient' in s_name:
                gradients_summaries += 1

        assert learning_rate_summaries > 0
        assert activations_summaries > 0
        assert gradients_summaries > 0
        assert loss_summaries > 0

    def test_return_estimator_spec(self):
        x = {'x': tf.placeholder(tf.float32, [2, 89])}
        y = tf.constant([[1], [1]])

        model = BaseModel(plx.Modes.TRAIN,
                          graph_fn=self.get_dummy_graph_fn(),
                          loss=LogLossConfig(),
                          optimizer=AdadeltaConfig(),
                          model_type=BaseModel.Types.CLASSIFIER,
                          metrics=[],
                          summaries=['learning_rate'],
                          name='test')

        assert isinstance(model(x, y, None, None), EstimatorSpec)

    def test_handle_train_mode(self):
        x = {'x': tf.placeholder(tf.float32, [2, 89])}
        y = tf.constant([[1], [1]])

        model = BaseModel(plx.Modes.TRAIN,
                          graph_fn=self.get_dummy_graph_fn(),
                          loss=LogLossConfig(),
                          optimizer=AdadeltaConfig(),
                          model_type=BaseModel.Types.CLASSIFIER,
                          metrics=[],
                          summaries=['learning_rate'],
                          name='test')
        specs = model(x, y, None, None)

        assert specs.loss is not None
        assert specs.predictions is not None
        assert 'losses' in specs.predictions
        assert specs.train_op is not None

    def test_handle_eval_mode(self):
        x = {'x': tf.placeholder(tf.float32, [2, 89])}
        y = tf.constant([[1], [1]])

        model = BaseModel(plx.Modes.EVAL, graph_fn=self.get_dummy_graph_fn(),
                          loss=LogLossConfig(),
                          optimizer=AdadeltaConfig(),
                          metrics=[],
                          model_type=BaseModel.Types.CLASSIFIER,
                          summaries=['learning_rate'],
                          name='test')
        specs = model(x, y, None, None)

        assert specs.loss is not None
        assert specs.predictions is not None
        assert 'losses' in specs.predictions
        assert specs.train_op is None

    def test_handle_predict_mode(self):
        x = {'x': tf.placeholder(tf.float32, [2, 89])}
        y = tf.constant([[1], [1]])

        model = BaseModel(plx.Modes.PREDICT, graph_fn=self.get_dummy_graph_fn(),
                          loss=LogLossConfig(),
                          optimizer=AdadeltaConfig(),
                          model_type=BaseModel.Types.CLASSIFIER,
                          metrics=[],
                          summaries=['learning_rate'],
                          name='test')
        specs = model(x, y, None, None)

        assert specs.loss is None
        assert specs.predictions is not None
        assert 'losses' not in specs.predictions
        assert specs.train_op is None
