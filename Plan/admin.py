from django.contrib import admin

from .models import *

class PlanFeatureAdmin(admin.TabularInline):
    model = PlanFeature

class MemberShipAdmin(admin.ModelAdmin):
   inlines = [PlanFeatureAdmin,]

admin.site.register(MemberShip,MemberShipAdmin)
