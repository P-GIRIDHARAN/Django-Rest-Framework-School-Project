from django.urls import include,path
from rest_framework.routers import DefaultRouter

from School_app import views
from School_app.views import StudentViewSet, TeacherCreateAPIView, SubjectMixins

router =DefaultRouter()
router.register(r'students',StudentViewSet)
urlpatterns = [
    path('api/', include(router.urls)),
    path('teacher/view/',views.ListTeachers.as_view()),
    path('teacher/view/<int:id>/', views.TeachersInfo.as_view()),
    path('teacher/', views.TeacherListAPIView.as_view()),
    path('teacher/create/',views.TeacherCreateAPIView.as_view()),
    path('teacher/<int:teacher_id>/',views.TeacherRetrieveAPIView.as_view()),
    path('teacher/delete/<int:teacher_id>/',views.TeacherDestroyAPIView.as_view()),
    path('subject/',views.SubjectMixins.as_view()),
]