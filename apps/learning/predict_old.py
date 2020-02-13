# -*- coding: utf-8 -*-
import os
import numpy as np
import scipy.sparse as sp
from django.conf import settings
from tensorflow.python.keras.applications.vgg19 import preprocess_input
from tensorflow.python.keras import Model
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.preprocessing import image
from sklearn.neighbors import NearestNeighbors

from configuration.models import LearningConfig
from learning.common import get_weights, get_vectors
from tensorflow.python.keras.applications.vgg19 import VGG19
import time
from configuration.models import SuperIndex
from catalogue.models import Category
test = SuperIndex.objects.first().vectors.name

LABEL_MAP = {
    0: (Category.COMPUTER_CHAIR, 'cabinet',),
    1: (Category.ARMCHAIR_OTTOMAN, 'chair'),
    2: (Category.ARMCHAIR_OTTOMAN, 'sofa'),
    3: (Category.TABLE, 'table')
}

VECTORS = get_vectors(LABEL_MAP)  # return example: {0: ('name', vectors))

# classification
MODEL_PATH = os.path.join(settings.DATADIR_ROOT, 'weights07-0.21.h5')

base_model = VGG19(weights=get_weights())


class Predict:
    CATEGORY_MODEL = load_model(MODEL_PATH)

    def __init__(self, search_instance):
        super().__init__()
        self.path = search_instance.image['ml'].path
        self.file = search_instance.image['ml']
        self.config = LearningConfig.get_solo()
        self.start_time = time.clock()
        self.last_time_point = 0
        self.category = None
        self.vectors = None
        self.articles = []

    def get_timing(self):
        return f"w_tm: {time.clock() - self.start_time}"

    def predict_category(self, model_image):

        model_image = model_image.reshape(
            (1, model_image.shape[0], model_image.shape[1], model_image.shape[2]))
        y = self.CATEGORY_MODEL.predict_classes(model_image)
        print(f'________________ {y} _____________________')
        # Ex value: ('name', vectors, articles)
        self.category, self.vectors, self.articles = VECTORS.get(y[0])

    def _vectorize(self, model):
        img = image.load_img(
            self.path or self.file, target_size=(224, 224))
        print(f'Open img file!: {self.get_timing()}')
        x = image.img_to_array(img)

        print(f'Img to array img file!: {self.get_timing()}')
        self.predict_category(x)
        print(f'Predict category!: {self.get_timing()}')
        x = np.expand_dims(x, axis=0)
        print(f'expand_dims!: {self.get_timing()}')
        x = preprocess_input(x)  # w_tm: 15.850202
        print(f'preprocess_input!: {self.get_timing()}')
        pred = model.predict(x)  # w_tm: 20.432673
        print(f'predict!: {self.get_timing()}')
        return pred.ravel()

    def _similar(self, vec, knn, list_data, n_neighbors=6):
        dist, indices = knn.kneighbors(
            vec.reshape(1, -1), n_neighbors=n_neighbors)
        dist, indices = dist.flatten(), indices.flatten()
        print(f'similar img id got!: {self.get_timing()}')
        return [(list_data[indices[i]], dist[i]) for i in range(len(indices))]

    def similarity(self, n_neighbors=6):
        # Read about fc1 here http://cs231n.github.io/convolutional-networks/
        model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)
        vec = self._vectorize(model)
        vectors = self.load_sparse_matrix()
        print(f'model without layers loaded: {self.get_timing()}')  # w_tm: 11.863167999999998
        knn = NearestNeighbors(metric='cosine', algorithm='brute')
        knn.fit(vectors)
        print(f'Training without control: {self.get_timing()}')
        print(f'Vector search img got: {self.get_timing()}')  # w_tm: 20.432828
        return self._similar(vec, knn, self.articles, n_neighbors)

    def load_sparse_matrix(self):
        y = self.vectors
        print(self.category)
        print(f'load_sparse_matrix: {self.get_timing()}')
        z = sp.coo_matrix((y['data'], (y['row'], y['col'])), shape=y['shape'])  # w_tm: 11.912833
        print(f'coo_matrix: {self.get_timing()}')
        return z
