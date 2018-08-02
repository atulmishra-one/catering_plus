from .base import *

STATIC_URL = 'http://127.0.0.1:8080/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = 'http://127.0.0.1:8080/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
