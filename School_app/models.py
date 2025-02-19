
from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=30)
    teacher_id=models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"

class Subject(models.Model):
    subject_name=models.CharField(max_length=20,default="MATHS")
    teacher_id=models.ForeignKey(Teacher,on_delete=models.CASCADE)

class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    subject=models.CharField(max_length=20,default="MATHS")
    mark=models.IntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class NonDeleted(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class SoftDelete(models.Model):
    is_deleted = models.BooleanField(default=False)
    everything = models.Manager()
    objects = NonDeleted()

    def soft_deleted(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True

class BusModel(SoftDelete):
    vehicle_model = models.CharField(max_length=20)
    bus_number = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.vehicle_model} {self.bus_number}"