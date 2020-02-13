# import logging
#
# import numpy as np
# from keras.applications import VGG19
# from keras.applications.vgg19 import preprocess_input
# from keras.engine import Model
# from keras.preprocessing import image
# from nearpy import Engine
# from nearpy.hashes import RandomBinaryProjections
# from nearpy.storage import RedisStorage
# from redis import Redis
# from tqdm import tqdm
#
# from catalogue.models import ProductImage, Category
# from learning.common import get_weights
#
# logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# # Create redis storage adapter
# redis_object = Redis(host='redis', port=6379, db=0, retry_on_timeout=True)
# redis_storage = RedisStorage(redis_object)
# # config = redis_storage.load_hash_configuration('Stolplit')
#
#
# class Vectorization(BaseLearning):
#     """Vectorization all image file"""
#     def __init__(self, queryset=None, new=True):
#         super().__init__()
#         self.queryset = queryset
#         self.files = []
#         self.articles = []
#         self.new = new
#
#     def get_queryset(self):
#         if not self.queryset:
#             self.queryset = ProductImage.objects.available()
#         return self.queryset
#
#     def get_files(self):
#         qs = self.get_queryset()
#         self.files = [
#             f'media/media/{path}' for path in qs.values_list('image', flat=True)
#         ]
#         self.articles = qs.values_list('article', flat=True)
#
#     def vectorize_all(self, model, px=224, n_dims=512,):  # 512
#
#         for category, category_name in Category.SUPER_CATEGORY_CHOICES:
#             print(category)
#             config = redis_storage.load_hash_configuration(category)
#             # Get hash config from redis
#
#             if config is None:
#                 # Config is not existing, create hash from scratch, with 10 projections
#                 lshash = RandomBinaryProjections(category, 10)
#             else:
#                 # Config is existing, create hash with None parameters
#                 lshash = RandomBinaryProjections(None, None)
#
#             # Apply configuration loaded from redis
#             # lshash.apply_config(config)
#             engine = Engine(n_dims, lshashes=[lshash], storage=redis_storage)
#
#             for product_image in tqdm(
#                     self.queryset.filter(category__super_category=category).distinct(),
#                     desc=f'Vectorization {category_name} category'):
#                 try:
#                     img = image.load_img(
#                         product_image.image['ml'].path, target_size=(px, px))
#                 except Exception as er:
#                     logger.error(f'VectorizeToRedis:IMAGE: {er}')
#                     product_image.status = ProductImage.BAD_FORMAT
#                     product_image.error = er
#                     product_image.save()
#                     continue
#
#                 x = image.img_to_array(img)
#                 x = np.expand_dims(x, axis=0)
#                 x = preprocess_input(x)  # w_tm: 15.850202
#                 pred = model.predict(x)  # w_tm: 20.432673
#                 engine.store_vector(pred.ravel(), data=product_image.article)
#
#             # Finally, store hash configuration in redis for later use
#             redis_storage.store_hash_configuration(lshash)
#
#         # Помечаем изображения как векторизованные
#         self.queryset.update(is_vectorized=True)
#
#     def execute(self):
#         # self.get_files()
#         base_model = VGG19(weights=self.get_weights())
#         # Read about fc1 here http://cs231n.github.io/convolutional-networks/
#         model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)
#         # Получаем матрицу с векторами изображений
#         self.vectorize_all(model, n_dims=4096)
