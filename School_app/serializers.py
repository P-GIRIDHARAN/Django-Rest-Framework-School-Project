
from rest_framework import serializers

from School_app.models import Student, Teacher, Subject


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=('id','first_name','last_name','subject','mark')
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=Teacher
        fields=('id','name','teacher_id')
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject
        fields=('id','teacher_name','subject_name')