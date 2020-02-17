# -*- coding: utf-8 -*-
import os
import numpy as np
import scipy.sparse as sp
from django.conf import settings
from tensorflow.python.keras.applications.vgg19 import preprocess_input
from tensorflow.python.keras.applications.vgg16 import preprocess_input as preprocess_input_vgg16
from tensorflow.python.keras import Model
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.preprocessing import image
from sklearn.neighbors import NearestNeighbors

from configuration.models import LearningConfig
from learning.common import get_weights, get_fitted_data
from tensorflow.python.keras.applications.vgg19 import VGG19
from tensorflow.python.keras.applications.vgg16 import VGG16
import time
from configuration.models import SuperIndex
from catalogue.models import Category
test = SuperIndex.objects.first().vectors.name

LABEL_MAP = {
    0: (Category.OTHER, 'cabinet',),
    1: (Category.CHAIR, 'chair'),
    2: (Category.COMPUTER_CHAIR, 'computer_chair'),
    3: (Category.SOFA_BED_CHAIR, 'sofa'),
    4: (Category.TABLE, 'table')
}

FITTED_DATA = get_fitted_data(LABEL_MAP)  # return example: {0: ('name', vectors))

# classification
MODEL_PATH = os.path.join(settings.DATADIR_ROOT, 'pre_trained_vgg16_b16_mixed_5.h5')

base_model = VGG19(weights=get_weights())
model_vgg16 = VGG16(include_top=False, weights=os.path.join(
    settings.DATADIR_ROOT, 'vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5'))
model_ml = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)


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
        self.knn_fitted = None
        self.articles = []

    def get_timing(self):
        return f"w_tm: {time.clock() - self.start_time}"

    def predict_category(self, img):
        model_image = image.img_to_array(img)
        model_image = model_image.reshape(
            (1, model_image.shape[0], model_image.shape[1], model_image.shape[2]))

        model_image = preprocess_input_vgg16(model_image)
        pred_y = model_vgg16.predict(model_image)
        y = self.CATEGORY_MODEL.predict_classes(pred_y)
        # Ex value: ('name', vectors, articles)
        self.category, self.knn_fitted, self.articles = FITTED_DATA.get(y[0])

    def _vectorize(self):
        img = image.load_img(
            self.path or self.file, target_size=(224, 224))
        print(f'Open img file!: {self.get_timing()}')
        x = image.img_to_array(img)

        print(f'Img to array img file!: {self.get_timing()}')
        self.predict_category(img)
        print(f'Predict category!: {self.get_timing()}')
        x = np.expand_dims(x, axis=0)
        print(f'expand_dims!: {self.get_timing()}')
        x = preprocess_input(x)  # w_tm: 15.850202
        print(f'preprocess_input!: {self.get_timing()}')
        pred = model_ml.predict(x)  # w_tm: 20.432673
        print(f'predict!: {self.get_timing()}')
        return pred.ravel()

    def _similar(self, vec, knn, list_data, n_neighbors=6):
        dist, indices = knn.kneighbors(
            vec.reshape(1, -1), n_neighbors=n_neighbors)
        dist, indices = dist.flatten(), indices.flatten()
        print(f'similar img id got!: {self.get_timing()}')
        return [(list_data[indices[i]], dist[i]) for i in range(len(indices))]

    def similarity(self, n_neighbors=6):
        vec = self._vectorize()
        return self._similar(vec, self.knn_fitted, self.articles, n_neighbors)
