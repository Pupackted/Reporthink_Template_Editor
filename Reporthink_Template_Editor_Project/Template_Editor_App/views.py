from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, "index.html")
def choose_template(request):
     return render(request, 'choose-template.html')
def edit_template(request):
     return render(request, 'edit-template.html')
def template_to_be_edited(request):
     return render(request, 'template-to-be-edited.html')