

from shadi.settings import *

from django.core.management.utils import get_random_secret_key

SECRET_KEY =SECRET_KEY = SECRET_KEY =get_random_secret_key() 
# load_dotenv('.env')
DEBUG = True

ALLOWED_HOSTS = ['52.72.255.130','localhost']


WSGI_APPLICATION = 'shadi.production.wsgi.application'


# Database

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME':'matrimony',
#         'USER': 'sanjitsinha',
#         'PASSWORD': 'sanjit@13145',
#         'HOST': '127.0.0.1',
#         'PORT': "5432"
#         }
   
           
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
if DEBUG:
    STATIC_URL = '/static/'
    STATIC_ROOT=os.path.join(BASE_DIR,'staticfile/')
    MEDIA_URL='/media/'
    MEDIA_ROOT=os.path.join(BASE_DIR,'mediafile/')
else:
    MEDIA_URL='/media/'
    MEDIA_ROOT=os.path.join(BASE_DIR,'mediafile/')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST= 'smtp.zoho.in'
EMAIL_PORT= 587
EMAIL_HOST_USER= 'zuhoo123@zohomail.in'
EMAIL_HOST_PASSWORD= 'Zuhoo@123'
EMAIL_USE_TLS= True