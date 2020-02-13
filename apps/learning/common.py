import os

import numpy as np
from django.conf import settings

from catalogue.models import Category
from configuration.models import SuperIndex


def get_weights():
    weights = settings.WEIGHTS
    if not os.path.isfile(weights):
        weights = 'imagenet'
    return weights


def get_vectors(label_map):
    """
    This method preparing a commutation map.
    :param label_map: as {
    (int(index in model ML): "super_category", str(Description)),
    0: ("sofa_bad", "sofa")
    }
    :return: {
    0: ('name', vectors, articles)
    }
    """
    vectors = {}
    for index_ml, value in label_map.items():
        index = SuperIndex.objects.filter(super_category=value[0]).first()
        # Checking index for existing.
        if index:
            path = index.vectors.path
            vectors[index_ml] = (value[1], np.load(path), index.article_list)
    return vectors
