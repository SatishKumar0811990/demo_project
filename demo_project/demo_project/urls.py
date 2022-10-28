
from django.contrib import admin
from django.urls import path, include
from authentication import views
from rest_framework.routers import DefaultRouter


prefix  = "api/v1/"
router = DefaultRouter()
router.register('allusers',views.Alluser,basename='allusers')
router.register('teacher',views.TeacherListView,basename='teacher')
router.register('courses',views.CourseListView,basename='courses')

   




urlpatterns = [
    path(prefix + 'admin/', admin.site.urls),
    path(prefix,include(router.urls)),
    path(prefix+'auth/', include('authentication.urls'),name="auth"),
    

]
