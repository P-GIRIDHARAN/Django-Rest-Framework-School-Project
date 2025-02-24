import datetime

import jwt
from django.contrib.auth import authenticate
import redis
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_redis import get_redis_connection
from rest_framework import viewsets, status, generics, mixins
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication

import time
from django.db import connection


from School_app.authentication import CustomJWTAuthentication
from School_app.models import Student, Teacher, Subject, BusModel
from School_app.serializers import StudentSerializer, TeacherSerializer, SubjectSerializer, BusSerializer
from School_app.utils import generate_jwt

redis_instance = redis.StrictRedis(host='127.0.0.1', port=6379, db=1)

class BusViewSet(viewsets.ModelViewSet):
    queryset = BusModel.objects.all()
    serializer_class = BusSerializer
# Create your views here.
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TeacherCreateAPIView(generics.CreateAPIView):
    model=Teacher
    serializer_class = TeacherSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        return super().create(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            teacher = serializer.save()

            teacher_url = reverse('teacher-detail', args=[teacher.teacher_id], request=request)

            return Response({
                'message': 'Teacher created successfully',
                'teacher_url': teacher_url
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ListTeachers(APIView):
    @method_decorator(cache_page(60*100))
    def get(self,request):
        teachers=Teacher.objects.all()
        serializer=TeacherSerializer(teachers,many=True)
        return Response(serializer.data)


    def post(self,request):
        serializer=TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
class TeachersInfo(APIView):
    def get(self,request,id):
        obj=Teacher.objects.get(id=id)
        serializer=TeacherSerializer(obj)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)

    def put(self, request, id):
        obj = Teacher.objects.get(id=id)
        serializer = TeacherSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self,request,id):
        obj=Teacher.objects.get(id=id)
        serializer=TeacherSerializer(obj,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        obj=Teacher.objects.get(id=id)
        obj.delete()
        return Response({"msg":"deleted"} ,status=status.HTTP_204_NO_CONTENT)


def log_db_queries(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        print(f"TOTAL COUNT: {len(connection.queries)}")
        duration = (end_time - start_time) * 1000  # Convert to milliseconds
        print(f"\nTotal Execution Time: {duration:.3f} ms")
        print("-" * 80)
        return res
    return wrapper

class TeacherListAPIView(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ('name', 'teacher_id',)
    ordering_fields = ('name',)
    search_fields = ('^name',)
    @log_db_queries
    def get_queryset(self):
        redis_instance = get_redis_connection("default")
        queryset = Teacher.objects.all()
        uncached_teachers = []

        for teacher in queryset:
            cache_key = f"teacher_{teacher.name}"  # Name-based cache key
            cached_teacher = redis_instance.get(cache_key)

            if cached_teacher:
                pass
            else:
                print(f"Storing {teacher.name} in Redis cache")
                teacher_data = {
                    "id": teacher.id,
                    "name": teacher.name,
                    "teacher_id": teacher.teacher_id
                }
                redis_instance.setex(cache_key, 300, json.dumps(teacher_data))  # Cache data for 5 minutes
                uncached_teachers.append(teacher)
        return queryset

class TeacherRetrieveAPIView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    lookup_field = 'teacher_id'

class TeacherDestroyAPIView(generics.DestroyAPIView):
    queryset = Teacher.objects.all()
    lookup_field = 'teacher_id'
    serializer_class = TeacherSerializer


class SubjectMixins(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset=Subject.objects.all()
    serializer_class=SubjectSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class PrivateView(generics.ListAPIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token = generate_jwt(user)
            return Response({'access_token': token}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)