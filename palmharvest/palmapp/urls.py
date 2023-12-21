from django.urls import path
from .import views

urlpatterns = [
    path('registeruser/', views.register, name="register_new_user"),
    path('branches/', views.allBranches, name="get_all_branches"),
    path('users/', views.allUsers, name="get_all_users"),
    path('images/', views.allimages, name="get_all_images"),
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
    path('sendemail/', views.sendEmail, name='send-email'),
    path('palmdetailed/', views.palmDetailed, name='palm-detailed'),
    path('deleteimage/<int:pk>/', views.deleteImage, name='delete_image'),
    path('createpalmdetail/', views.createPalmDetail, name='create_palm_detail'),
    path('deletepalmdetail/<int:pk>/', views.deletePalmDetail, name='delete_palm_detail'),
    path('getPalmDetails/<int:image_id>/', views.getPalmDetails, name='get_palm_details'),
    path('getpalmlist/',views.getImageWithPalmDetails, name='get_image_with_palm_details'),
    path('getpalmdetailssummary/', views.getPalmDetailsSummary, name='get_palm_details_summary'),
    path('getpalmssummarybybranch/', views.getPalmsSummaryByBranch, name='get_palms_summary_by_branch'),
    path('getharvesterscountbybranch/', views.getHarvestersCountByBranch, name="get_harvesters_count_by_branch"),
    path('harvesterpalmconnectedsummary/', views.harvesterPalmConnectedSummary, name="manager_harvester_users"),
    path('allyearmonthswithimagecount/', views.allYearMonthsWithImageAndDataCount, name='all-year-months-with-image-count'),
    path('logout/',views.logout, name="logout")

]