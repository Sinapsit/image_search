"""Development server settings."""
from .base import *


DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

ALLOWED_HOSTS = ('stolplit-nn.spider.ru',)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USERNAME'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOSTNAME'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

# Machine learning
VECTORS_PATH = '/home/HOSTING/stolplit_nn/project/datadir/vectors/image_vectors.npz'
WEIGHTS = '/home/HOSTING/stolplit_nn/project/datadir/vgg19_weights_tf_dim_ordering_tf_kernels.h5'