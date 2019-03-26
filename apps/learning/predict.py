# -*- coding: utf-8 -*-

import numpy as np
import scipy.sparse as sp
from django.conf import settings
from keras.applications.vgg19 import preprocess_input
from keras.engine import Model
from keras.preprocessing import image
from sklearn.neighbors import NearestNeighbors

from configuration.models import LearningConfig
from learning.common import BaseLearning


# def _vectorize(path, model):
#     img = image.load_img(path, target_size=(224, 224))
#     x = image.img_to_array(img)
#     x = np.expand_dims(x, axis=0)
#     x = preprocess_input(x)
#     pred = model.predict(x)
#     return pred.ravel()
#
#
# def _similar(vec, knn, filenames, n_neighbors=6):
#     dist, indices = knn.kneighbors(vec.reshape(1, -1), n_neighbors=n_neighbors)
#     dist, indices = dist.flatten(), indices.flatten()
#     return [(filenames[indices[i]], dist[i]) for i in range(len(indices))]
#
#
# def load_predictor(dir_name):
#     filenames = open(config.images_order(dir_name), 'r').readline().split(',')
#     vecs = load_sparse_matrix(config.vectors_path(dir_name))
#     base_model = VGG19(weights='imagenet')
#     # Read about fc1 here http://cs231n.github.io/convolutional-networks/
#     model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)
#     knn = NearestNeighbors(metric='cosine', algorithm='brute')
#     knn.fit(vecs)
#
#     def similarity(file_path, n_neighbors=6):
#         vec = _vectorize(file_path, model)
#         return _similar(vec, knn, filenames, n_neighbors)
#
#     return similarity
#
#
# def random(owner_id):
#     filenames = open(config.images_order(owner_id), 'r').readline().split(',')
#
#     def rf():
#         return np.random.choice(filenames)
#
#     return rf
#
#
# def download(url):
#     f = "/tmp/images/{}".format(str(uuid4()))
#     request.urlretrieve(url, f)
#     return f


class Predict(BaseLearning):

    def __init__(self, path=None, file=None, list_content='filename'):
        self.path = path
        self.file = file
        self.config = LearningConfig.get_solo()
        self.list_content = list_content

    def _vectorize(self, model):
        img = image.load_img(self.path or self.file, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        pred = model.predict(x)
        return pred.ravel()

    def _similar(self, vec, knn, list_data, n_neighbors=6):
        dist, indices = knn.kneighbors(vec.reshape(1, -1), n_neighbors=n_neighbors)
        dist, indices = dist.flatten(), indices.flatten()
        return [(list_data[indices[i]], dist[i]) for i in range(len(indices))]

    def similarity(self, n_neighbors=6):
        with self.graph.as_default():
            vecs = self.load_sparse_matrix()

            # Read about fc1 here http://cs231n.github.io/convolutional-networks/
            model = Model(inputs=self.base_model.input, outputs=self.base_model.get_layer('fc1').output)
            knn = NearestNeighbors(metric='cosine', algorithm='brute')
            knn.fit(vecs)
            list_data = self.config.filename_list
            if self.list_content == 'article':
                list_data = self.config.article_list

            vec = self._vectorize(model)
            print(type(vec))
            return self._similar(vec, knn, list_data, n_neighbors)

    def load_sparse_matrix(self):
        y = np.load(settings.VECTORS_PATH)
        z = sp.coo_matrix((y['data'], (y['row'], y['col'])), shape=y['shape'])
        return z
