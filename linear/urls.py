from django.urls import path

from . import views

app_name = "linear"

urlpatterns = [
    path("webhook/", views.webhook),
    path("import/", views.import_issues, name="import_issues"),
]
