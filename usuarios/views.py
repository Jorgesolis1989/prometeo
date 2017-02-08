from django.shortcuts import render

# Create your views here.


def usuario_home(request):
    return render(request, 'base-usuario.html')
