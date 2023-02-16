from .base import *


SECRET_KEY =config('PRO_SECRET_KEY')


ALLOWED_HOSTS=[str(host) for host in config('PRODUCTION_ALLOWED_HOSTS').split(",")]

DEBUG=config('PRODUCTION_DEBUG')
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print("production")
print(DEBUG)
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


# SERVER Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':config('PRO_DB_NAME'),
        'USER': config('PRO_DB_USER'),
        'PASSWORD': config('PRO_DB_PASSWORD'),
        'HOST': config('PRO_DB_HOST'),
        'PORT': config('PORT')
        }
   
           
}

STATIC_URL='/static/'
MEDIA_URL='media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media_dir')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=True
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True


"""CORS CONFIGRATION"""
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOWED_ORIGINS=config('WHITE_LIST', cast=lambda v: [s.strip() for s in v.split(',')])
CORS_ORIGIN_WHITELIST = config('WHITE_LIST', cast=lambda v: [s.strip() for s in v.split(',')])
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = config('WHITE_LIST', cast=lambda v: [s.strip() for s in v.split(',')])
CORS_ALLOW_METHODS = ["DELETE","GET","OPTIONS","PATCH","POST","PUT"]
CORS_ALLOW_HEADERS = ["accept","accept-encoding","authorization","content-type","dnt","origin",
    "user-agent","x-csrftoken","x-requested-with"]
        

