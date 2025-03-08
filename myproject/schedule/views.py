from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView

from schedule.models import Department, Teacher


def home(request):
    return render(request, 'home.html')


class AddDepartment(CreateView):
    model = Department
    template_name = 'add_department.html'
    success_url = reverse_lazy('department_list')
    fields = '__all__'


class DepartmentListView(ListView):
    model = Department
    template_name = 'department_list.html'
    context_object_name = 'departments'


class DepartmentDeleteView(DeleteView):
    model = Department
    template_name = 'department_confirm_delete.html'
    success_url = reverse_lazy('department_list')


class AddTeacher(CreateView):
    model = Teacher
    template_name = 'add_teacher.html'
    success_url = reverse_lazy('teacher_list')
    fields = '__all__'


class TeacherListView(ListView):
    model = Teacher
    template_name = 'teacher_list.html'
    context_object_name = 'teachers'

    def get_queryset(self):
        queryset = super().get_queryset()
        department = self.request.GET.get('department', None)
        if department:
            queryset = queryset.filter(department__name=department)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.values_list('name',
                                                                flat=True).distinct()
        context['selected_department'] = self.request.GET.get('department', '')
        return context


class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name = 'teacher_confirm_delete.html'
    success_url = reverse_lazy('teacher_list')


class About(CreateView):
    model = Teacher
    template_name = 'about.html'
    fields = '__all__'


class Contacts(CreateView):
    model = Teacher
    template_name = 'contact.html'
    fields = '__all__'
