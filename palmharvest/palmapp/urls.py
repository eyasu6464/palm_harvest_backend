from django.urls import path
from .import views

urlpatterns = [
    path('registeruser/', views.register, name="register_new_user"),
    path('branches/', views.allBranches, name="get_all_branches"),
    path('users/', views.allUsers, name="get_all_branches"),
    path('images/', views.allimages, name="get_all_branches"),
]