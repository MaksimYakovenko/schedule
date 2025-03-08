from django.urls import path
from . import views
from .views import AddDepartment, AddTeacher, About, Contacts, TeacherListView, \
    DepartmentListView, TeacherDeleteView, DepartmentDeleteView, AddAudience, \
    AudienceListView, AudienceDeleteView

urlpatterns = [
    path('', views.home, name='home'),
    path('add_department/', AddDepartment.as_view(), name='add_department'),
    path('add_teacher/', AddTeacher.as_view(), name='add_teacher'),
    path('add_audience/', AddAudience.as_view(), name='add_audience'),
    path('add_lesson/', AddTeacher.as_view(), name='add_lesson'),
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
]
