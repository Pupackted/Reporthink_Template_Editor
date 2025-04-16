from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
  path('choose-template/', views.choose_template, name='choose_template'),
  path('edit-template/', views.edit_template, name='edit_template'),
    
 path('edit/<int:template_id>/', views.edit_template_view, name='edit_template'),
]


# path("template-to-be-edited/", views.template_to_be_edited, name="template_to_be_edited"),
