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

from keras.applications import VGG19
import time

from keras import backend as K


class Predict(BaseLearning):

    def __init__(self, path=None, file=None, list_content='filename'):
        super().__init__()
        self.path = path
        self.file = file
        self.config = LearningConfig.get_solo()
        self.list_content = list_content
        self.start_time = time.clock()
        self.last_time_point = 0

    def get_timing(self):
        return f"w_tm: {time.clock() - self.start_time}"

    def _vectorize(self, model):

        img = image.load_img(self.path or self.file, target_size=(224, 224))
        print(f'Open img file!: {self.get_timing()}')
        x = image.img_to_array(img)
        print(f'Img to array img file!: {self.get_timing()}')
        x = np.expand_dims(x, axis=0)
        print(f'expand_dims!: {self.get_timing()}')
        x = preprocess_input(x)  # w_tm: 15.850202
        print(f'preprocess_input!: {self.get_timing()}')
        pred = model.predict(x)  # w_tm: 20.432673
        print(f'predict!: {self.get_timing()}')
        K.clear_session()
        return pred.ravel()

    def _similar(self, vec, knn, list_data, n_neighbors=6):
        dist, indices = knn.kneighbors(vec.reshape(1, -1), n_neighbors=n_neighbors)
        dist, indices = dist.flatten(), indices.flatten()
        print(f'similar img id got!: {self.get_timing()}')
        return [(list_data[indices[i]], dist[i]) for i in range(len(indices))]

    def similarity(self, n_neighbors=6):
        base_model = VGG19(weights=self.get_weights())  # w_tm: 5.669065000000001
        print(f'Base model loaded: {self.get_timing()}')
        vecs = self.load_sparse_matrix()  # w_tm: 11.862487999999999

        # Read about fc1 here http://cs231n.github.io/convolutional-networks/
        model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)
        model._make_predict_function()
        print(f'model without layers loaded: {self.get_timing()}')  # w_tm: 11.863167999999998
        knn = NearestNeighbors(metric='cosine', algorithm='brute')
        knn.fit(vecs)
        print(f'Training without control: {self.get_timing()}')
        list_data = self.config.filename_list

        if self.list_content == 'article':
            list_data = self.config.article_list
        print(f'Got list data: {self.get_timing()}')
        vec = self._vectorize(model)
        print(f'Vector search img got: {self.get_timing()}')  # w_tm: 20.432828

        return self._similar(vec, knn, list_data, n_neighbors)

    def load_sparse_matrix(self):
        y = np.load(settings.VECTORS_PATH)  # w_tm: 5.493172
        print(f'load_sparse_matrix: {self.get_timing()}')
        z = sp.coo_matrix((y['data'], (y['row'], y['col'])), shape=y['shape'])  # w_tm: 11.912833
        print(f'coo_matrix: {self.get_timing()}')
        return z
