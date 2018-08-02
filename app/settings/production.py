from .base import *

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'catering',
        'HOST': '127.0.0.1',
        'USER': 'root',
        'PASSWORD': 'root123'
    }
}

ALLOWED_HOSTS = (
    '142.93.94.64:8080',
    '142.93.94.64',
)