from django.urls import path,include #,re_path,include
from django.views.generic import TemplateView
# from rest_framework.schemas import get_schema_view
# from django.conf.urls import url
# from django.conf.urls import url
# from rest_framework import routers
from api import views as view_profile
from api.userprofile import views as views_usr

# API
urlpatterns = [       
    path('docs/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
    
    # path('', include(router.urls)),
    path('profiles/', view_profile.ProfileList.as_view()),
    path('profile/', view_profile.ProfileByToken.as_view()),
    path('profile/<int:pk>/', view_profile.ProfileDetail.as_view()),
    path('profile/avatar/<int:pk>/', view_profile.AvatarUpdate.as_view()),  
    
    #Account
    path('user/register/', views_usr.RegistrationAPIView.as_view()),
    path('user/update/<int:pk>/', views_usr.UpdateFirstLast_Name.as_view()),        
    path('user/activate/<uidb64>/<token>/', views_usr.Activate, name='activate'),      
]