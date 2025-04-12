from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
  path('choose-template/', views.choose_template, name='choose_template'),
  path('edit-template/', views.edit_template, name='edit_template'),
]