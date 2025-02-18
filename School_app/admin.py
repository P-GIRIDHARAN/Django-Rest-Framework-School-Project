from django.contrib import admin

from School_app.models import Student, Teacher, BusModel

# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(BusModel)
