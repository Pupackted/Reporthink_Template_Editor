from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Public access
    path("", views.index, name="index"),

    # Login / logout
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    # Signup (custom view)
    path('signup/', views.signup, name='signup'),

    # Logged in users only
    path('choose-template/', views.choose_template, name='choose_template'),
    path('edit-template-part/<int:part_id>/', views.edit_template_part, name='edit_template_part'),
    # path('edit/<int:template_id>/', views.edit_template_view, name='edit_template'),

    # NEW: Step 1 - Create a document from a template
    path('template/<int:template_id>/create/', views.create_user_document_from_template, name='create_user_document'),
    # NEW: Step 2 - Edit a specific document
    path('document/<int:document_id>/edit/', views.edit_document_view, name='edit_document_view'),
    # NEW: URL to save a specific document
    path('document/<int:document_id>/save/', views.save_user_document, name='save_user_document'), 
    # NEW: URL to update the document's name
    path('update-document-name/<int:document_id>/', views.update_document_name, name='update_document_name'),
    # Update your profile and delete views to use the new model/IDs
    path('profile/', views.user_profile, name='user_profile'),
    path('document/<int:document_id>/delete/', views.delete_user_document, name='delete_user_document'),


    # path('update-template-name/<int:template_id>/', views.update_template_name, name='update-template-name'),
    path('update-document-name/<int:document_id>/', views.update_document_name, name='update_document_name'),

    # Admin only
    path('create-template/', views.create_template, name='create_template'),
    path('add-template-part/<int:template_id>/', views.add_template_part, name='add_template_part'),
    path('set-cover-part/<int:template_id>/', views.set_cover_part, name='set_cover_part'),

    # User template edits
    # path('save-user-edit/<int:template_id>/', views.save_user_template_edit, name='save_user_template_edit'),
    # path('save-user-template-edit/<int:template_id>/', views.save_user_template_edit, name='save_user_template_edit'),
    path('document/<int:document_id>/save/', views.save_user_document, name='save_user_document'),
    path('load-user-edit/<int:template_id>/', views.load_user_template_edit, name='load_user_template_edit'),
    path('profile/', views.user_profile, name='user_profile'),
    # path('delete-user-edit/<int:edit_id>/', views.delete_user_template_edit, name='delete_user_template_edit'),
    path('document/<int:document_id>/delete/', views.delete_user_document, name='delete_user_document'),

]
