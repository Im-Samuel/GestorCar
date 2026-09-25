from django.urls import path

from . import views

app_name = "sitio1"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("cm/", views.cargamosMensaje, name="mensaje"),
]
