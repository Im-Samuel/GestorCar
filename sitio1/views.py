from django.http import HttpResponse

#Creamos una vista que devuelva un mensaje de bienvenida al usuario.
def inicio(request):
    return HttpResponse("Hola, bienvenido a mi sitio 1 web.")
# Create your views here.

def cargamosMensaje(request):
    return HttpResponse("Hola, bienvenido a mi sitio 1 web. Esta es la segunda vista.")
