from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(City)
admin.site.register(State)
admin.site.register(SaveOTP)
admin.site.register(BannerImage)
admin.site.register(HomeScreenImage)
class PersonAdmin(admin.ModelAdmin):
    list_display=['id','matrimony_id','name','phone_number',"reg_date"]
    list_editable=['matrimony_id']
    list_filter=['reg_date']
class FriendRequestsAdmin(admin.ModelAdmin):
    list_display=['id','profile','requested_matrimony_id','request_status','status']
    list_editable=['status']
admin.site.register(Person,PersonAdmin)
admin.site.register(FriendRequests,FriendRequestsAdmin)