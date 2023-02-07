from .base import *
from decouple import config

SECRET_KEY =config('DEV_SECRET_KEY')


ALLOWED_HOSTS=[str(host) for host in config('DEV_ALLOWED_HOSTS').split(",")]

DEBUG=config('DEV_DEBUG')

STATIC_URL='/static/'
MEDIA_URL='media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media_dir')


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':config('NAME'),
        'USER': config('USER'),
        'PASSWORD': config('PASSWORD'),
        'HOST': config('HOST'),
        'PORT': config('PORT')
        }
   
           
}







CORS_ALLOW_ALL_ORIGINS=True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_ALLOW_ALL = True 
CORS_ALLOWED_ORIGINS=(
    'http://localhost:3000',
    'http://localhost:4200',
)
CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'http://localhost:4200',
)


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'