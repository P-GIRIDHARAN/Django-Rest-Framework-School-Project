
from rest_framework import serializers

from School_app.models import Student, Teacher, Subject, BusModel
def character_less_than_15(value):
    if len(value)>15:
        raise serializers.ValidationError("Value cannot be greater than 15 character")

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    first_name=serializers.CharField(max_length=20,validators=[character_less_than_15])
    class Meta:
        model=Student
        fields=('id','url','first_name','last_name','subject','mark')
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=Teacher
        fields=('id','name','teacher_id')
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject
        fields=('id','teacher_id','subject_name')

class BusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=BusModel
        fields=('url','id','vehicle_model','bus_number')