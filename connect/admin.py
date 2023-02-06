from django.contrib import admin
from .models import *
# Register your models here.
class UpdateRequestsAdmin(admin.ModelAdmin):
    list_display=['id','request_status','update_field_name']
    
class DocumentUploadAdmin(admin.ModelAdmin):
    list_display=['id','upload_status','name_of_document',"profile","status"]
    list_editable=['status']
admin.site.register(UpdateRequests,UpdateRequestsAdmin)
admin.site.register(DocumentUpload,DocumentUploadAdmin)