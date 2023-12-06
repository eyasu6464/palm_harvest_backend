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
    path('getbranch/<str:pk>/', views.getbranch, name='get_one_branch_by_id'),
    path('allbranchnames/', views.allBranchNames, name='all_branch_names_list'),
    path('inactiveusers/', views.inactiveUsers, name='list_of_inactive_users'),
    path('activateaccount/<int:id>/', views.activateAccount, name='activate-account'),
    path('deactivateaccount/<int:id>/', views.deactivateAccount, name='deactivate-account'),
    path('updatebranch/<int:pk>/', views.updateBranch, name='update_branch_info'),
    path('deletebranch/<int:pk>/', views.deleteBranch, name='delete_branch_by_id'),
    path('updateprofile/', views.updateProfile, name="Update_Profile"),
    path('changepassword/', views.changePassword, name="change _user_password"),
    path('forgetpassword/', views.forgetPassword, name='reset_user_password'),
    path('reset-password/<str:uidb64>/<str:token>/', views.resetPassword, name='reset_password'),
    path('image/<int:pk>/', views.getImageDetails, name='image-details'),

]