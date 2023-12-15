from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from django.views.generic import TemplateView
from palmapp.views import CustomTokenObtainPairView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('palmapp.urls')),
    path('api/token/',CustomTokenObtainPairView.as_view()),
    path('api/token/verify/', TokenVerifyView.as_view()),
]
