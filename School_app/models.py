from tkinter.constants import CASCADE

from django.db import models
from django.db.models import CharField


# Create your models here.

class Teacher(models.Model):
    name = models.CharField(max_length=30)
    teacher_id=models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"

class Subject(models.Model):
    subject_name=models.CharField(max_length=20,default="MATHS")
    teacher_name=models.ForeignKey(Teacher,on_delete=models.CASCADE)

class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    subject=models.CharField(max_length=20,default="MATHS")
    mark=models.IntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"