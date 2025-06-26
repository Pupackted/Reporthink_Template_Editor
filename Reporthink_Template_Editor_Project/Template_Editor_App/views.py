import os
import json

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import TemplateForm, TemplatePartForm, SignUpForm
from .models import Template
# from .models import UserTemplateEdit  # Uncomment if needed
from .models import Template, UserDocument




def is_admin(user):
    return user.is_staff  # or user.is_superuser depending on your admin setup


# def index(request):
#     templates = Template.objects.all()
#     # Kirim template_id default, misal template pertama atau None
#     first_template_id = templates.first().id if templates.exists() else None
#     return render(request, 'index.html', {
#         'templates': templates,
#         'template_form': TemplateForm(),
#         'template_part_form': TemplatePartForm(),
#         'some_template_id': first_template_id,  # Kirim ke template
#     })

def index(request):
    search_query = request.GET.get('q', '')  # get search query from URL parameter 'q'
    if search_query:
        templates = Template.objects.filter(
            Q(name__icontains=search_query),
            cover_part__isnull=False
        )
    else:
        templates = Template.objects.filter(cover_part__isnull=False)

    first_template_id = templates.first().id if templates.exists() else None
    return render(request, 'index.html', {
        'templates': templates,
        'template_form': TemplateForm(),
        'template_part_form': TemplatePartForm(),
        'some_template_id': first_template_id,
        'search_query': search_query,
    })


@login_required
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


@login_required
def edit_template(request):
     return render(request, 'edit-template.html')
@login_required
def template_to_be_edited(request):
     return render(request, 'template-to-be-edited.html')





# --- 1. OLD View: The Editor Was Loading a Template Directly ---

# @login_required
# def edit_template_view(request, template_id):
#     template = get_object_or_404(Template, id=template_id)
    
#     # Get all possible parts for this template
#     parts = template.parts.all()

#     # Create a dictionary with info for all parts, keyed by the part's base name
#     # This is the crucial information the frontend was missing.
#     all_parts_info = {
#         part.name: {
#             'thumbnailSrc': part.thumbnail.url,
#             'htmlFileUrl': part.html_file.url
#         } for part in parts
#     }

#     # Load user edits if they exist
#     user_edits = None
#     if request.user.is_authenticated:
#         try:
#             # We fetch the entire saved object, which will contain our new structure
#             user_edits = UserTemplateEdit.objects.get(user=request.user, template=template)
#         except UserTemplateEdit.DoesNotExist:
#             user_edits = None

#     context = {
#         'template': template,
#         'parts': parts,
#         # Pass the raw saved data (or an empty dict)
#         'user_edits': user_edits.edited_parts if user_edits else {},
#         # Pass the new all_parts_info dictionary
#         'all_parts_info': all_parts_info,
#     }

#     return render(request, 'edit-template.html', context)


# --- 3. REPLACED View: The Editor Now Loads a Document ---
@login_required
def edit_document_view(request, document_id):
    # Fetch the specific document, ensuring it belongs to the current user for security
    document = get_object_or_404(UserDocument, id=document_id, user=request.user)
    template = document.template # Get the base template from the document
    
    parts = template.parts.all()
    all_parts_info = {
        part.name: {
            'thumbnailSrc': part.thumbnail.url,
            'htmlFileUrl': part.html_file.url
        } for part in parts
    }

    context = {
        'document': document, # Pass the document object
        'template': template, # Still pass the base template info
        'parts': parts,
        'user_edits': document.edited_parts, # The saved data is on the document itself
        'all_parts_info': all_parts_info,
    }
    return render(request, 'edit-template.html', context)




@login_required
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

# --- REPLACED View: update template name ---
# @csrf_exempt
# def update_template_name(request, template_id):
#     if request.method == "POST":
#         new_name = request.POST.get('name')
#         print("Received name:", new_name)  # Debugging
#         if new_name:
#             template = get_object_or_404(Template, id=template_id)
#             template.name = new_name
#             template.save()
#             return JsonResponse({'status': 'ok'})
#     return JsonResponse({'status': 'error'}, status=400)

# --- 5. REPLACED View: Update the Document Name ---
@csrf_exempt
@login_required
def update_document_name(request, document_id):
    if request.method == "POST":
        new_name = request.POST.get('name')
        if new_name:
            document = get_object_or_404(UserDocument, id=document_id, user=request.user)
            document.name = new_name
            document.save()
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)




# forms to upload and create templates and template parts

@user_passes_test(is_admin)
def create_template(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.cover_part = None  # No cover part yet
            template.save()
            return redirect('add_template_part', template_id=template.id)
    else:
        form = TemplateForm()
    return render(request, 'create_template.html', {'form': form})


@user_passes_test(is_admin)
def add_template_part(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    parts = template.parts.all()  # Get existing parts

    if request.method == 'POST':
        form = TemplatePartForm(request.POST, request.FILES)
        if form.is_valid():
            part = form.save(commit=False)
            part.template = template
            part.save()
            if 'add_another' in request.POST:
                return redirect('add_template_part', template_id=template.id)
            else:
                return redirect('set_cover_part', template_id=template.id)
    else:
        form = TemplatePartForm()

    return render(request, 'add_template_part.html', {
        'form': form,
        'template': template,
        'parts': parts,  # Pass parts to template
    })


# set cover part
@user_passes_test(is_admin)
def set_cover_part(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    parts = template.parts.all()
    
    if request.method == 'POST':
        cover_id = request.POST.get('cover_part')
        if cover_id:
            cover_part = get_object_or_404(template.parts, id=cover_id)
            template.cover_part = cover_part
            template.save()
            return redirect('index')  # or wherever you want
        
    return render(request, 'set_cover_part.html', {'template': template, 'parts': parts})



# authentication views

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in immediately after signup
            return redirect('choose_template')  # Redirect to next page after signup
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})



## Save user edits to templates

# --- REPLACED View: Save User Edits to a Template ---
# @login_required
# @csrf_exempt
# def save_user_template_edit(request, template_id):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             edited_parts = data.get('edited_parts', {})
#             user = request.user
#             template = get_object_or_404(Template, id=template_id)

#             obj, created = UserTemplateEdit.objects.get_or_create(
#                 user=user, template=template,
#                 defaults={'edited_parts': edited_parts}
#             )
#             if not created:
#                 obj.edited_parts = edited_parts
#                 obj.save()
#             return JsonResponse({'status': 'ok'})
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'error': str(e)}, status=400)
#     return JsonResponse({'status': 'error', 'error': 'Invalid method'}, status=400)

# --- 4. REPLACED View: Save a Document ---

@login_required
@csrf_exempt
def save_user_document(request, document_id):
    if request.method == "POST":
        try:
            document = get_object_or_404(UserDocument, id=document_id, user=request.user)
            data = json.loads(request.body)

            # FIX: Reconstruct the 'edited_parts' dictionary from the received data
            order = data.get('order', [])
            pages = data.get('pages', {})
            document.edited_parts = {'order': order, 'pages': pages}

            # This part for saving the name is already correct
            new_name = data.get('name')
            if new_name:
                document.name = new_name

            # Save everything at once
            document.save()
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'error': 'Invalid method'}, status=400)



@login_required
def load_user_template_edit(request, template_id):
    user = request.user
    template = get_object_or_404(Template, id=template_id)
    try:
        obj = UserTemplateEdit.objects.get(user=user, template=template)
        return JsonResponse({'status': 'ok', 'edited_parts': obj.edited_parts})
    except UserTemplateEdit.DoesNotExist:
        return JsonResponse({'status': 'not_found', 'edited_parts': {}})



# User profile view to show saved template edits
# --- OLD View: User Profile ---
# @login_required
# def user_profile(request):
#     # Get all saved template edits for this user
#     saved_edits = request.user.template_edits.select_related('template').all()

#     return render(request, 'user_profile.html', {
#         'saved_edits': saved_edits,
#     })

# --- 6. UPDATED View: User Profile ---
@login_required
def user_profile(request):
    # Fetch all documents owned by this user
    saved_documents = request.user.documents.select_related('template').order_by('-last_modified').all()
    return render(request, 'user_profile.html', {
        'saved_documents': saved_documents,
    })



# delete user template edit
# --- OLD View: Delete a User Template Edit ---
# @login_required
# def delete_user_template_edit(request, edit_id):
#     edit = get_object_or_404(UserTemplateEdit, id=edit_id, user=request.user)
#     if request.method == "POST":
#         edit.delete()
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             return JsonResponse({'status': 'ok'})
#         return redirect('user_profile')
#     return JsonResponse({'status': 'error', 'error': 'Invalid request'}, status=400)

# --- 7. UPDATED View: Delete a Document ---
@login_required
def delete_user_document(request, document_id):
    document = get_object_or_404(UserDocument, id=document_id, user=request.user)
    if request.method == "POST":
        document.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'ok'})
        return redirect('user_profile')
    return JsonResponse({'status': 'error', 'error': 'Invalid request'}, status=400)



# --- 2. NEW View: Create a Document and Redirect to Editor ---
@login_required
def create_user_document_from_template(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    
    # Create a default name, like "Template Name - 1", "Template Name - 2", etc.
    existing_count = UserDocument.objects.filter(user=request.user, template=template).count()
    doc_name = f"{template.name} - {existing_count + 1}"

    # Create the new document instance
    document = UserDocument.objects.create(
        user=request.user,
        template=template,
        name=doc_name,
        edited_parts={} # Start with empty edits
    )
    
    # Redirect to the editor for this new document
    return redirect('edit_document_view', document_id=document.id)
