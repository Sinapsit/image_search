import logging
import os
import numpy as np
import scipy.sparse as sp
from django.conf import settings
from tensorflow.python.keras import Model
from tensorflow.python.keras.applications.vgg19 import VGG19
from tensorflow.python.keras.applications.vgg19 import preprocess_input
from tensorflow.python.keras.preprocessing import image
from tqdm import tqdm
from utils.methods import generate_code
from catalogue.models import ProductImage, Category
from configuration.models import SuperIndex
from learning.common import get_weights

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class Vectorization:
    """Vectorization all image file"""

    def __init__(self, queryset=None, super_category=None):
        super().__init__()
        self.queryset = queryset
        self.super_category = super_category
        self.files = []
        self.articles = []
        self.vectors_filename = self.get_vectors_path()
        base_model = VGG19(weights=get_weights())
        # Read about fc1 here http://cs231n.github.io/convolutional-networks/
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

    def get_vectors_path(self):
        return os.path.join(
            settings.VECTORS_DIR,
            f'vectors_{generate_code()}_{self.super_category or "all"}.npz'
        )

    def get_queryset(self):
        if not self.queryset:
            self.queryset = ProductImage.objects.available()
        if self.super_category:
            self.queryset = self.queryset.filter(
                category__super_category=self.super_category).distinct()
        return self.queryset

    def get_files(self):
        qs = self.get_queryset()
        for product in tqdm(qs, desc='Prepare URL/ARTICLE list'):
            self.files.append(product.image["ml"].path)
            self.articles.append(product.article)

    def vectorize_all(self, px=224, n_dims=512, batch_size=50):
        logger.info("Will vectorize")
        min_idx = 0
        max_idx = min_idx + batch_size
        total_max = len(self.files)
        # Создаем пустую матрицу по кол_во фалов строк на n_dims столбцов
        lil_matrix = sp.lil_matrix((len(self.files), n_dims))

        logger.info("Total: {}".format(len(self.files)))
        while min_idx < total_max - 1:
            logger.info(f'start {min_idx}')
            # Создаем пустой массив заполненный нулями
            image_data = np.zeros(
                ((max_idx - min_idx), px, px, 3)
            )
            # For each file in the batch, load as row into images_data
            i = 0
            for i in tqdm(range(min_idx, max_idx), desc='Load image data'):
                file = self.files[i]
                try:
                    img = image.load_img(file, target_size=(px, px))
                    img_array = image.img_to_array(img)
                    image_data[i - min_idx, :, :, :] = img_array
                except Exception as e:
                    logger.info(e)
            max_idx = i
            logger.info(f'PREPROCESS INPUT')
            image_data = preprocess_input(image_data)
            logger.info(f'START PREDICT')
            these_preds = self.model.predict(image_data)
            shp = ((max_idx - min_idx) + 1, n_dims)
            lil_matrix[min_idx:max_idx + 1, :] = these_preds.reshape(shp)
            min_idx = max_idx
            max_idx = np.min((max_idx + batch_size, total_max))
            logger.info(f'FINISH PREDICT')
        return lil_matrix

    def save(self, arr, filename):
        with open(filename, 'w') as fd:
            fd.write(','.join(arr))

    def execute(self):
        self.get_files()

        # Получаем матрицу с векторами изображений
        vectors = self.vectorize_all(n_dims=4096)

        # Сохраняем разряженную матрицу в файл
        self.save_sparse_matrix(vectors)

        # Помечаем существующие картинки, для возможности восстановления выборки.
        # self.get_queryset().update(is_vectorized=True)
        logger.info('Finished')

    def save_sparse_matrix(self, matrix):
        logger.info(f'SAVE MATRIX')
        matrix_coo = matrix.tocoo()
        row = matrix_coo.row
        col = matrix_coo.col
        data = matrix_coo.data
        shape = matrix_coo.shape
        np.savez(self.vectors_filename, row=row, col=col, data=data, shape=shape)

        # save list of filename
        ml_conf, _ = SuperIndex.objects.update_or_create(
            super_category=self.super_category,
            defaults={
                "filename_list": list(self.files),
                "article_list": list(self.articles)
            }
        )
        ml_conf.vectors.name = self.vectors_filename.replace(settings.MEDIA_ROOT+'/', '')
        ml_conf.save()
