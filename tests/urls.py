from django.contrib import admin
from django.urls import path
from django.urls.conf import include

admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("linear/", include("linear.urls")),
    path("anymail/", include("anymail.urls")),
]
