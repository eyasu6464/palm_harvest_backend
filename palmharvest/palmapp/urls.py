from django.urls import path
from .import views

urlpatterns = [
    path('registeruser/', views.register, name="register_new_user"),
    path('branches/', views.allBranches, name="get_all_branches"),
    path('users/', views.allUsers, name="get_all_branches"),
    path('images/', views.allimages, name="get_all_branches"),
    path('registerbranch/', views.registerBranch, name='register_branch'),
    path('uploadimage/', views.uploadImage, name="Upload_image"),
    path('userinformation/', views.userInfo, name="user_information"),
    path('getbranch/<str:pk>/', views.getbranch, name='get_one_branch_by_id')
]