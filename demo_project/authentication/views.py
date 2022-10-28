from django.shortcuts import render
from yaml import serialize
from rest_framework import generics, status, views, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from .serializers import RegisterSerializer, LoginSerializer,AlluserSerializer, LogoutSerializer,ChangePasswordSerializer,CourseSerializer,InstructorSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from rest_framework.generics import ListAPIView
from django.http import HttpResponse,JsonResponse
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRenderer
from rest_framework.parsers import JSONParser
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django.urls import reverse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
import io
from rest_framework.renderers import JSONRenderer
from .models import  Course,Teacher
from rest_framework import viewsets





class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        
        return Response(user_data, status=status.HTTP_201_CREATED)



class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)








class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)
    

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)






class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)
    

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








class WriteByAdminOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        print('insidnde has permission', request.user)
        user = request.user
        if request.method == 'GET':
            return True

        if request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE':
            if user.is_superuser:
                return True

        return False


class Alluser(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser,WriteByAdminOnlyPermission]
    queryset=User.objects.all()
    serializer_class = AlluserSerializer

class Userdetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,permissions.IsAdminUser)
    serializer_class = AlluserSerializer
    queryset=User.objects.all()

class TeacherListView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InstructorSerializer
    queryset = Teacher.objects.all()


class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InstructorSerializer
    queryset = Teacher.objects.all()


class CourseListView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
