import os

import numpy as np
from django.conf import settings
import scipy.sparse as sp
from catalogue.models import Category
from configuration.models import SuperIndex
from sklearn.neighbors import NearestNeighbors


def get_weights():
    weights = settings.WEIGHTS
    if not os.path.isfile(weights):
        weights = 'imagenet'
    return weights


def get_fitted_data(label_map):
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
            y = np.load(path)
            v = sp.coo_matrix((y['data'], (y['row'], y['col'])), shape=y['shape'])
            knn = NearestNeighbors(metric='cosine', algorithm='brute')
            knn.fit(v)
            vectors[index_ml] = (value[1], knn, index.article_list)
    return vectors
