from django.urls import path,include #,re_path,include
from django.views.generic import TemplateView
# from rest_framework.schemas import get_schema_view
# from django.conf.urls import url
# from django.conf.urls import url
# from rest_framework import routers
from api import views

# API
urlpatterns = [       
    path('docs/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
    # path('', include(router.urls)),
    path('snippets/', views.SnippetList.as_view()),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
    path('avatar/<int:pk>/', views.AvatarUpdate.as_view()),    
    
]