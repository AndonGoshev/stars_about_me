

from django.contrib import admin
from django.urls import path, include

from stars_about_me.core import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urls)),
]
