from django.shortcuts import render, get_object_or_404
from .models import Template


# Create your views here.
from django.http import HttpResponse


def index(request):
    templates = Template.objects.all()  # Or however you load your templates
    return render(request, 'index.html', {'templates': templates})

# def choose_template(request):
#     templates = Template.objects.all()
#     return render(request, 'choose-template.html', {'templates': templates})

def choose_template(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    return render(request, 'choose-template.html', {'template': template})


def edit_template(request):
     return render(request, 'edit-template.html')
def template_to_be_edited(request):
     return render(request, 'template-to-be-edited.html')

# def editor_view(request, template_id):
#     template_obj = get_object_or_404(Template, id=template_id)

#     with open(template_obj.html_file.path, 'r') as file:
#         html_content = file.read()

#     return render(request, 'editor.html', {
#         'template': template_obj,
#         'html_content': html_content
#     })

# def editor_view(request, template_id):
#     template = get_object_or_404(Template, pk=template_id)
#     html_path = template.html_file.path

#     with open(html_path, 'r', encoding='utf-8') as f:
#         html_content = f.read()

#     return render(request, 'edit-template.html', {
#         'template': template,
#         'html_content': html_content
#     })

def edit_template_view(request, template_id):
    template = get_object_or_404(Template, id=template_id)

    # Read the contents of the uploaded HTML file
    html_path = template.html_file.path
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    context = {
        'template': template,
        'html_content': html_content,
    }

    return render(request, 'edit-template.html', context)


# not sure about this
# def choose_template(request):
#     templates = Template.objects.all()
#     return render(request, 'choose-template.html', {'templates': templates})
