"""
WSGI config for shadi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os


from django.core.wsgi import get_wsgi_application
#from django.apps import apps
# models_list=apps.get_models()
# model_list=[]
# for model in models_list:
    
#     model_list.append(model.__name__)
# print(model_list)   
# for model in models_list:
    
#     if model.__name__=="Bookmark":
#         all_field=model._meta.get_fields()
#         for field in all_field:
#             print(field.name)
#         print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    
#     else:
#         pass
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shadi.production.settings')

application = get_wsgi_application()
