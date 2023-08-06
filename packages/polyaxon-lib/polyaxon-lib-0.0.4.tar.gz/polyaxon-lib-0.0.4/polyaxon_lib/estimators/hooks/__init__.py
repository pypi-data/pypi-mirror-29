# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

from polyaxon_lib.estimators.hooks.general_hooks import (
    GENERAL_HOOKS,
    FinalOpsHook,
    GlobalStepWaiterHook,
    StopAfterNEvalsHook,
    NanTensorHook,
)
from polyaxon_lib.estimators.hooks.step_hooks import (
    STEP_HOOKS,
    StepLoggingTensorHook,
    StopAtStepHook,
    StepCheckpointSaverHook,
    StepCounterHook,
    StepSummarySaverHook,
)
from polyaxon_lib.estimators.hooks.episode_hooks import (
    EPISODE_HOOKS,
    EpisodeLoggingTensorHook,
    StopAtEpisodeHook,
    EpisodeSummarySaverHook,
    EpisodeCheckpointSaverHook,
    EpisodeCounterHook,
)

HOOKS = OrderedDict([
    ('FinalOpsHook', FinalOpsHook),
    ('GlobalStepWaiterHook', GlobalStepWaiterHook),
    ('StopAfterNEvalsHook', StopAfterNEvalsHook),
    ('NanTensorHook', NanTensorHook),

    ('StepLoggingTensorHook', StepLoggingTensorHook),
    ('StopAtStepHook', StopAtStepHook),
    ('StepCheckpointSaverHook', StepCheckpointSaverHook),
    ('StepCounterHook', StepCounterHook),
    ('StepSummarySaverHook', StepSummarySaverHook),

    ('EpisodeLoggingTensorHook', EpisodeLoggingTensorHook),
    ('StopAtEpisodeHook', StopAtEpisodeHook),
    ('EpisodeSummarySaverHook', EpisodeSummarySaverHook)
])
