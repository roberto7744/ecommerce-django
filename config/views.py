from django.shortcuts import render

def index(request):
    """Página de inicio simple para la raíz del sitio."""
    return render(request, 'index.html')