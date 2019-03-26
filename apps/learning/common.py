from keras.applications import VGG19
import os
from django.conf import settings
import tensorflow as tf


def get_weights():
    weights = settings.WEIGHTS
    if not os.path.isfile(weights):
        weights = 'imagenet'
    return weights


class BaseLearning:
    graph = tf.get_default_graph()
    base_model = VGG19(weights=get_weights())

