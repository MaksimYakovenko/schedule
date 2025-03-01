from django.urls import path
from . import views
from .views import AddDepartment, AddTeacher, About, Contacts

urlpatterns = [
    path('', views.home, name='home'),
    path('add_department/', AddDepartment.as_view(), name='add_department'),
    path('add_teacher/', AddTeacher.as_view(), name='add_teacher'),
    path('about/', About.as_view(), name='about'),
    path('contacts/', Contacts.as_view(), name='contacts'),
    path('teachers/', TeacherListView.as_view(), name='teacher_list'),
]
