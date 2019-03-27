import numpy as np
import scipy.sparse as sp
from django.conf import settings
from keras.applications.vgg19 import preprocess_input
from keras.engine import Model
from keras.preprocessing import image

from catalogue.models import ProductImage
from configuration.models import LearningConfig
from learning.common import BaseLearning
import tensorflow as tf
from keras.applications import VGG19

class Vectorization(BaseLearning):
    """Vectorization all image file"""
    def __init__(self, queryset=None):
        super().__init__()
        self.queryset = queryset
        self.files = []
        self.articles = []
        self.vectors_filename = settings.VECTORS_PATH

    def get_queryset(self):
        if not self.queryset:
            self.queryset = ProductImage.objects.available()
        return self.queryset

    def get_files(self):
        qs = self.get_queryset()
        self.files = [
            f'media/media/{path}' for path in qs.values_list('image', flat=True)
        ]
        self.articles = qs.values_list('article', flat=True)

    def vectorize_all(self, model, px=224, n_dims=512, batch_size=512):  # 512
        print("Will vectorize")
        min_idx = 0
        max_idx = min_idx + batch_size
        total_max = len(self.files)
        # Создаем пустую матрицу по кол_во фалов строк на n_dims столбцов
        lil_matrix = sp.lil_matrix((len(self.files), n_dims))

        print("Total: {}".format(len(self.files)))
        while min_idx < total_max - 1:
            print(min_idx)
            # Создаем пустой массив заполненный нулями
            image_data = np.zeros(((max_idx - min_idx), px, px, 3))
            # For each file in batch, load as row into image_data
            i = 0
            for i in range(min_idx, max_idx):
                file = self.files[i]
                try:
                    img = image.load_img(file, target_size=(px, px))
                    img_array = image.img_to_array(img)
                    image_data[i - min_idx, :, :, :] = img_array
                except Exception as e:
                    print(e)
            max_idx = i
            image_data = preprocess_input(image_data)
            these_preds = model.predict(image_data)
            shp = ((max_idx - min_idx) + 1, n_dims)
            lil_matrix[min_idx:max_idx + 1, :] = these_preds.reshape(shp)
            min_idx = max_idx
            max_idx = np.min((max_idx + batch_size, total_max))
        return lil_matrix

    def save(self, arr, filename):
        with open(filename, 'w') as fd:
            fd.write(','.join(arr))

    def execute(self):
        self.get_files()
        base_model = VGG19(weights=self.get_weights())
        # Read about fc1 here http://cs231n.github.io/convolutional-networks/
        model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

        # Получаем матрицу с векторами изображений
        vectors = self.vectorize_all(model, n_dims=4096)

        # Сохраняем разряженную матрицу в файл
        self.save_sparse_matrix(vectors)

        # Помечаем существующие картинки, для возможности восстановления выборки.
        # self.get_queryset().update(is_vectorized=True)
        print('Finished')

    def save_sparse_matrix(self, matrix):
        matrix_coo = matrix.tocoo()
        row = matrix_coo.row
        col = matrix_coo.col
        data = matrix_coo.data
        shape = matrix_coo.shape
        np.savez(self.vectors_filename, row=row, col=col, data=data, shape=shape)

        # save list of filename
        ml_conf = LearningConfig.get_solo()
        ml_conf.filename_list = list(self.files)
        ml_conf.article_list = list(self.articles)
        with open(self.vectors_filename, 'rb') as npz_file:
            ml_conf.file.save(name='image_vectors.npz', content=npz_file, save=False)

        ml_conf.save()
