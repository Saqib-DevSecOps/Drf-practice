from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from  rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from . import views

router = DefaultRouter()
router.register('studentsapi', views.StudentsApi, basename='student')

urlpatterns = [
    path('student/', views.StudentCreateList.as_view()),
    path('student/<str:pk>', views.StudentRetrieveUpdateDestroy.as_view()),
    path('auth/token/',TokenObtainPairView.as_view(),name='token_pair'),
    path('auth/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('auth/token/verify/',TokenVerifyView.as_view(),name='token_verify'),
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls')),
]
