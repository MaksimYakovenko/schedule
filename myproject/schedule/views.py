from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from schedule.models import Department, Teacher


def home(request):
    return render(request, 'home.html')


class AddDepartment(CreateView):
    model = Department
    template_name = 'add_department.html'
    fields = '__all__'


class AddTeacher(CreateView):
    model = Teacher
    template_name = 'add_teacher.html'
    success_url = reverse_lazy('teacher_list')
    fields = '__all__'



class About(CreateView):
    model = Teacher
    template_name = 'about.html'
    fields = '__all__'


class Contacts(CreateView):
    model = Teacher
    template_name = 'contact.html'
    fields = '__all__'