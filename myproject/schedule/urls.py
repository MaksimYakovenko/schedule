from django.urls import path
from . import views
from .views import (AddDepartment, AddTeacher, About, Contacts, TeacherListView, \
    DepartmentListView, TeacherDeleteView, DepartmentDeleteView, AddAudience, \
    AudienceListView, AudienceDeleteView, TeacherUpdateView, \
    DepartmentUpdateView, AudienceUpdateView, AddLesson, LessonDeleteView,
                    LessonUpdateView, schedule_view)

urlpatterns = [
    path('', views.home, name='home'),
    path('add_department/', AddDepartment.as_view(), name='add_department'),
    path('add_teacher/', AddTeacher.as_view(), name='add_teacher'),
    path('add_audience/', AddAudience.as_view(), name='add_audience'),
    path('add_lesson/', AddLesson.as_view(), name='add_lesson'),
    path('about/', About.as_view(), name='about'),
    path('contacts/', Contacts.as_view(), name='contacts'),
    path('teachers/', TeacherListView.as_view(), name='teacher_list'),
    path('departments/', DepartmentListView.as_view(), name='department_list'),
    path('audiences/', AudienceListView.as_view(), name='audience_list'),
    path('teachers/<int:pk>/delete/', TeacherDeleteView.as_view(), name='teacher_delete'),
    path('departments/<int:pk>/delete/', DepartmentDeleteView.as_view(),
         name='department_delete'),
    path('audiences/<int:pk>/delete/', AudienceDeleteView.as_view(),
         name='audience_delete'),
    path('lessons/<int:pk>/delete/', LessonDeleteView.as_view(),
         name='audience_delete'),
    path('teachers/<int:pk>/edit/', TeacherUpdateView.as_view(), name='teacher_edit'),
    path('departments/<int:pk>/edit/', DepartmentUpdateView.as_view(),
         name='department_edit'),
    path('audiences/<int:pk>/edit/', AudienceUpdateView.as_view(),
         name='audience_edit'),
    path('lessons/<int:pk>/edit/', LessonUpdateView.as_view(),
         name='lesson_edit'),
    path('schedule/', schedule_view, name='schedule'),
]
