from django.shortcuts import render

from .models import *

# Create your views here.

def index(request):
    proteins = Protein.objects.all()
    return render(request, 'proteindata/index.html', {'proteins' : proteins})
