# -*- coding: utf-8 -*-

import time

import numpy as np
from nearpy import Engine
from nearpy.hashes import RandomBinaryProjections
from nearpy.storage import RedisStorage
from nearpy.filters import DistanceThresholdFilter, NearestFilter, UniqueFilter
from redis import Redis
from tensorflow.python.keras import Model
from tensorflow.python.keras.applications.vgg19 import VGG19
from tensorflow.python.keras.applications.vgg19 import preprocess_input
from tensorflow.python.keras.preprocessing import image

from configuration.models import LearningConfig
from learning.common import get_weights
from catalogue.models import Category

# Create redis storage adapter
redis_object = Redis(host='redis', port=6379, db=0, retry_on_timeout=True)
redis_storage = RedisStorage(redis_object)
base_model = VGG19(weights=get_weights())


class Predict:

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
        return pred.ravel()

    def _similar(self, vec, knn, list_data, n_neighbors=6):
        dist, indices = knn.kneighbors(vec.reshape(1, -1), n_neighbors=n_neighbors)
        dist, indices = dist.flatten(), indices.flatten()
        print(f'similar img id got!: {self.get_timing()}')
        return [(list_data[indices[i]], dist[i]) for i in range(len(indices))]

    def similarity(self, n_neighbors=6):
         # w_tm: 5.669065000000001
        print(f'Base model loaded: {self.get_timing()}')
        # with graph.as_default():
        # vecs = self.load_sparse_matrix()  # w_tm: 11.862487999999999

        # Read about fc1 here http://cs231n.github.io/convolutional-networks/
        model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)
        print(f'model without layers loaded: {self.get_timing()}')  # w_tm: 11.863167999999998
        # knn = NearestNeighbors(metric='cosine', algorithm='brute')
        # knn.fit(vecs)
        print(f'Training without control: {self.get_timing()}')
        # list_data = self.config.filename_list

        # if self.list_content == 'article':
        #     list_data = self.config.article_list
        print(f'Got list data: {self.get_timing()}')
        vec = self._vectorize(model)
        print(f'Vector search img got: {self.get_timing()}')  # w_tm: 20.432828
        # return self._similar(vec, knn, list_data, n_neighbors)

        # category = self.get_category()
        config = redis_storage.load_hash_configuration(Category.COMPUTER_CHAIR)
        if config is None:
            # Config is not existing, create hash from scratch, with 10 projections
            lshash = RandomBinaryProjections(Category.COMPUTER_CHAIR, 10)
        else:
            # Config is existing, create hash with None parameters
            lshash = RandomBinaryProjections(None, None)
            # Apply configuration loaded from redis

        lshash.apply_config(config)

        engine = Engine(
            4096,
            lshashes=[lshash],
            storage=redis_storage,
            vector_filters=[
                # DistanceThresholdFilter(10),
                NearestFilter(10),
                # UniqueFilter()
            ]
        )
        return [[article, distance] for a, article, distance in engine.neighbours(vec)]
