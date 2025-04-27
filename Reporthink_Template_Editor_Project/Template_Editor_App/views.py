from django.shortcuts import render, get_object_or_404
from .models import Template
from django.http import HttpResponse
from django.conf import settings
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse



# Create your views here.


def index(request):
    templates = Template.objects.all()
    print("Templates:", templates)  # Debugging
    return render(request, 'index.html', {'templates': templates})



def choose_template(request):
    templates = Template.objects.all()
    selected_id = request.GET.get('selected_id')

    selected_template = None
    if selected_id:
        selected_template = Template.objects.filter(id=selected_id).first()

    return render(request, 'choose-template.html', {
        'templates': templates,
        'selected_id': selected_id,
        'template': selected_template  # <== add this
    })



def edit_template(request):
     return render(request, 'edit-template.html')
def template_to_be_edited(request):
     return render(request, 'template-to-be-edited.html')


# def edit_template_view(request, template_id):
#     print("template id:")
#     print(template_id)  # Debugging

#     template = get_object_or_404(Template, id=template_id)
#     print("template.html_file: ")
#     print(template.html_file)  # Debugging

#     if not template.html_file:
#         return HttpResponse("No HTML file specified for this template.", status=400)
    
#     file_path = os.path.join(settings.MEDIA_ROOT, template.html_file.replace('media/', '', 1))

#     print("file_path: ")
#     print(file_path)  # Debugging
#     try:
#       with open(file_path, 'r', encoding='utf-8') as f:
#         html_content = f.read()
#     except FileNotFoundError:
#         return HttpResponse("HTML file not found.", status=404)

#     context = {
#         'template': template,
#         'html_content': html_content,  # Optional, only if your HTML uses it
#     }

#     return render(request, template.get_template_path(), context)

# def edit_template_part(request, part_id):
#     part = get_object_or_404(TemplatePart, id=part_id)
#     print(template.parts.all()) 
#     return render(request, 'edit-template-part.html', {'part': part})

# def edit_template_view(request, template_id):
#     print("template id:")
#     print(template_id)  # Debugging

#     template = get_object_or_404(Template, id=template_id)
    
#     cover_part = template.cover_part  # Get the cover part
#     parts = template.parts.all()

#     if not parts:
#         return HttpResponse("No parts found for this template.", status=404)

#     context = {
#         'template': template,
#         'cover_part': cover_part,
#         'parts': parts,  # <-- keep everything
#     }

#     return render(request, 'edit-template.html', context)

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

def edit_template_view(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    cover_part = template.cover_part

    if not cover_part:
        return HttpResponse("No cover page selected for this template.", status=404)

    file_path = cover_part.html_file.path

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        return HttpResponse("HTML file not found.", status=404)

    parts = template.parts.all()  # Get all parts related to this template

    context = {
        'template': template,
        'cover_part': cover_part,
        'html_content': html_content,
        'parts': parts,  # Pass the parts
    }

    return render(request, 'edit-template.html', context)


def edit_template_part(request, part_id):
    part = get_object_or_404(TemplatePart, id=part_id)
    print("Editing part:", part)

    # Load the actual HTML content of the part
    html_content = ''
    if part.html_file:
        try:
            file_path = os.path.join(settings.MEDIA_ROOT, part.html_file.name)
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
        except FileNotFoundError:
            return HttpResponse("HTML file for this part not found.", status=404)

    context = {
        'part': part,
        'html_content': html_content,
    }

    return render(request, 'edit-template-part.html', context)

# @csrf_exempt
# def update_template_name(request, template_id):
#     if request.method == "POST":
#         new_name = request.POST.get('name')
#         print("Received name:", new_name)  # for debug
#         if new_name:
#             template = get_object_or_404(Template, id=template_id)
#             template.name = new_name
#             template.save()
#             return JsonResponse({'status': 'ok'})
#     return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def update_template_name(request, template_id):
    if request.method == "POST":
        new_name = request.POST.get('name')
        print("Received name:", new_name)  # Debugging
        if new_name:
            template = get_object_or_404(Template, id=template_id)
            template.name = new_name
            template.save()
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)

