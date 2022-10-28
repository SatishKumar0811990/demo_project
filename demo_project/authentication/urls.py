from django.urls import path,include
from .views import RegisterView, LogoutAPIView,LoginAPIView,ChangePasswordView,CourseListView,CourseDetailView,TeacherDetailView,Userdetail
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)





urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('allusers/<int:pk>', Userdetail.as_view(), name='user-detail'),
    path('courses/<int:pk>', CourseDetailView.as_view(), name='course-detail'),
    path('teacher/<int:pk>', TeacherDetailView.as_view(),
         name='teacher-detail'),
   
    
    
]
