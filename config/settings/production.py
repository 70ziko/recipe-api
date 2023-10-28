from .base import *
import django_heroku


DEBUG = False
ALLOWED_HOSTS = ['recipe-backend-api.herokuapp.com', 'reactipe-1fcd5773eea7.herokuapp.com', 'localhost', '127.0.0.1']

INSTALLED_APPS += [
    'cloudinary_storage',
    'cloudinary',
]

# Media
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Cloudinary configs
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': config('CLOUDINARY_API_SECRET'),
    'API_SECRET': config('CLOUDINARY_API_KEY')
}

django_heroku.settings(locals())
