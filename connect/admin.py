from django.contrib import admin
from .models import *
# Register your models here.
class UpdateRequestsAdmin(admin.ModelAdmin):
    list_display=['id','request_status','update_field_name']
admin.site.register(UpdateRequests,UpdateRequestsAdmin)