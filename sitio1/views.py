from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def inicio(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


def cargamosMensaje(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        "Hola, bienvenido a GestorCar. Esta es la segunda vista de sitio1."
    )
