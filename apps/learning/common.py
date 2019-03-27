from keras.applications import VGG19
import os
from django.conf import settings


class BaseLearning:
    """"""
    def get_weights(self):
        weights = settings.WEIGHTS
        if not os.path.isfile(weights):
            weights = 'imagenet'
        return weights
