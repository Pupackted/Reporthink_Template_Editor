from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

  path('choose-template/', views.choose_template, name='choose_template'),

    path('edit-template-part/<int:part_id>/', views.edit_template_part, name='edit_template_part'),
     
  path('edit/<int:template_id>/', views.edit_template_view, name='edit_template'),
  path('update-template-name/<int:template_id>/', views.update_template_name, name='update-template-name'),
     path('create-template/', views.create_template, name='create_template'),
    path('add-template-part/<int:template_id>/', views.add_template_part, name='add_template_part'),
    path('set-cover-part/<int:template_id>/', views.set_cover_part, name='set_cover_part'),

]

