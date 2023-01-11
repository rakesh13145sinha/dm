"""shadi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static



if settings.DEBUG:

    urlpatterns = [
        path('admin/', admin.site.urls),
        # reurl(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
        path('api/v1/',
                include([
                    path('account/',include('account.urls')),
                    path('plan/',include('Plan.urls')),
                    path('vendor/',include('Eventmanagement.urls')),
                    path('search/',include('search.urls')),
                    path('connect/',include('connect.urls'))
                ])
            )
    ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    from django.views.static import serve
    
    urlpatterns = [
        re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
        path('api/v1/',
                include([
                    path('account/',include('account.urls')),
                    path('plan/',include('Plan.urls')),
                    path('vendor/',include('Eventmanagement.urls')),
                    path('search/',include('search.urls')),
                    path('connect/',include('connect.urls'))
                ])
            )
    ]
    
    
    
    #url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),