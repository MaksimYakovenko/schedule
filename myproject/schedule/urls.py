from django.urls import path
from . import views
from .views import AddDepartment, AddTeacher, About, Contacts, TeacherListView, \
    DepartmentListView, TeacherDeleteView, DepartmentDeleteView

urlpatterns = [
    path('', views.home, name='home'),
    path('add_department/', AddDepartment.as_view(), name='add_department'),
    path('add_teacher/', AddTeacher.as_view(), name='add_teacher'),
    path('about/', About.as_view(), name='about'),
    path('contacts/', Contacts.as_view(), name='contacts'),
    path('teachers/', TeacherListView.as_view(), name='teacher_list'),
    path('departments/', DepartmentListView.as_view(), name='department_list'),
    path('teachers/<int:pk>/delete/', TeacherDeleteView.as_view(), name='teacher_delete'),
    path('departments/<int:pk>/delete/', DepartmentDeleteView.as_view(),
         name='department_delete'),
]
