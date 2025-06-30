from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    # --- Public Views ---
    # The main landing page for all visitors.
    path("", views.index, name="index"),

    # --- Authentication ---
    # URLs for handling user login, logout, and registration.
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('signup/', views.signup, name='signup'),

    # --- Core Application Flow (For Logged-In Users) ---
    # The main journey for a user creating and managing their documents.
    path('my-works/', views.user_profile, name='user_profile'),
    path('choose-template/', views.choose_template, name='choose_template'),
    
    # Step 1: Create a new document from a template
    path('template/<int:template_id>/create/', views.create_user_document_from_template, name='create_user_document'),
    
    # Step 2: Edit, save, rename, and delete the user's document
    # path('edit-template-part/<int:part_id>/', views.edit_template_part, name='edit_template_part'),
    path('document/<int:document_id>/edit/', views.edit_document_view, name='edit_document_view'),
    path('document/<int:document_id>/save/', views.save_user_document, name='save_user_document'),
    path('document/<int:document_id>/delete/', views.delete_user_document, name='delete_user_document'),
    path('update-document-name/<int:document_id>/', views.update_document_name, name='update_document_name'),

    # --- Admin & Template Management ---
    # URLs for staff/admins to create and manage the base templates.
    path('create-template/', views.create_template, name='create_template'),
    path('add-template-part/<int:template_id>/', views.add_template_part, name='add_template_part'),
    path('set-cover-part/<int:template_id>/', views.set_cover_part, name='set_cover_part'),
    


]









# from django.urls import path
# from . import views
# from django.contrib.auth import views as auth_views

# urlpatterns = [
#     # Public access
#     path("", views.index, name="index"),

#     # Login / logout
#     path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

#     # Signup (custom view)
#     path('signup/', views.signup, name='signup'),

#     # Logged in users only
#     path('choose-template/', views.choose_template, name='choose_template'),
#     path('edit-template-part/<int:part_id>/', views.edit_template_part, name='edit_template_part'),
#     # path('edit/<int:template_id>/', views.edit_template_view, name='edit_template'),

#     # NEW: Step 1 - Create a document from a template
#     path('template/<int:template_id>/create/', views.create_user_document_from_template, name='create_user_document'),
#     # NEW: Step 2 - Edit a specific document
#     path('document/<int:document_id>/edit/', views.edit_document_view, name='edit_document_view'),
#     # NEW: URL to save a specific document
#     path('document/<int:document_id>/save/', views.save_user_document, name='save_user_document'), 
#     # NEW: URL to update the document's name
#     path('update-document-name/<int:document_id>/', views.update_document_name, name='update_document_name'),
#     # Update your profile and delete views to use the new model/IDs
#     path('profile/', views.user_profile, name='user_profile'),
#     path('document/<int:document_id>/delete/', views.delete_user_document, name='delete_user_document'),


#     # path('update-template-name/<int:template_id>/', views.update_template_name, name='update-template-name'),
#     path('update-document-name/<int:document_id>/', views.update_document_name, name='update_document_name'),

#     # Admin only
#     path('create-template/', views.create_template, name='create_template'),
#     path('add-template-part/<int:template_id>/', views.add_template_part, name='add_template_part'),
#     path('set-cover-part/<int:template_id>/', views.set_cover_part, name='set_cover_part'),

#     # User template edits

#     path('document/<int:document_id>/save/', views.save_user_document, name='save_user_document'),
#     path('load-user-edit/<int:template_id>/', views.load_user_template_edit, name='load_user_template_edit'),
#     path('profile/', views.user_profile, name='user_profile'),
 
#     path('document/<int:document_id>/delete/', views.delete_user_document, name='delete_user_document'),

# ]

