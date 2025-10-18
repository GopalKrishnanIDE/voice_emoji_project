from django.contrib import admin
from django.urls import path, include
from .views import home  # import the new view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('recordings.urls')),
    path('', home),  # root path
]
