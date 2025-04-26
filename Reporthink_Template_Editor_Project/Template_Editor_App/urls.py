from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
  # path('choose-template/', views.choose_template, name='choose_template'),
  # in urls.py
  # path('choose-template/<int:template_id>/', views.choose_template, name='choose_template'),
  # path('edit-template/', views.edit_template, name='edit_template'),

  path('choose-template/', views.choose_template, name='choose_template'),

    path('edit-template-part/<int:part_id>/', views.edit_template_part, name='edit_template_part'),

  path('edit/<int:template_id>/', views.edit_template_view, name='edit_template'),
  path('update-template-name/<int:template_id>/', views.update_template_name, name='update-template-name'),

]

# path('choose/', views.choose_template, name='choose_template'),


# path("template-to-be-edited/", views.template_to_be_edited, name="template_to_be_edited"),
