from django.contrib.auth import login, authenticate
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, status, generics, mixins
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.reverse import reverse
from School_app.models import Student, Teacher, Subject, BusModel
from School_app.serializers import StudentSerializer, TeacherSerializer, SubjectSerializer, BusSerializer
from rest_framework.pagination import LimitOffsetPagination


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

    def post(self, request,*args, **kwargs):
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

class TeacherListAPIView(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    name="teacher-list"
    filterset_fields=(
        'name',
        'teacher_id',
    )
    ordering_fields = (
        'name',
    )
    search_fields = (
        '^name',
    )



class TeacherRetrieveAPIView(generics.RetrieveAPIView):
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