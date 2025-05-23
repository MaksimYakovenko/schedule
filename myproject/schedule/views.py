from datetime import datetime
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.core.exceptions import ValidationError
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from schedule.models import (Department, Teacher, Classroom, Lesson, Group,
                             Subject, Semester, ScheduleEntry, Session)


def home(request):
    teacher_count = Teacher.objects.count()
    department_count = Department.objects.count()
    lessons_count = ScheduleEntry.objects.count()
    classroom_count = Classroom.objects.count()
    return render(request, 'home.html', {
        'teacher_count': teacher_count,
        'department_count': department_count,
        'lessons_count': lessons_count,
        'classroom_count': classroom_count,
    })

class AddDepartment(CreateView):
    model = Department
    template_name = 'add_department.html'
    success_url = reverse_lazy('department_list')
    fields = '__all__'


class AddSubject(CreateView):
    model = Subject
    template_name = 'add_subject.html'
    success_url = reverse_lazy('subject_list')
    fields = '__all__'


class AddSession(CreateView):
    model = Session
    template_name = 'add_session.html'
    success_url = reverse_lazy('session_list')
    fields = '__all__'


class AddSemester(CreateView):
    model = Semester
    template_name = 'add_semester.html'
    success_url = reverse_lazy('semester_list')
    fields = '__all__'


class SemesterListView(ListView):
    model = Semester
    template_name = 'semester_list.html'
    context_object_name = 'semesters'


class LessonListView(ListView):
    model = Lesson
    template_name = 'lesson_list.html'
    context_object_name = 'lessons'


class SessionListView(ListView):
    model = Session
    template_name = 'session_list.html'
    context_object_name = 'sessions'


class SessionDeleteView(DeleteView):
    model = Session
    template_name = 'session_confirm_delete.html'
    success_url = reverse_lazy('session_list')
    fields = '__all__'


class SessionUpdateView(UpdateView):
    model = Session
    template_name = 'edit_session.html'
    fields = '__all__'
    success_url = reverse_lazy('session_list')

class SemesterDeleteView(DeleteView):
    model = Semester
    template_name = 'semester_confirm_delete.html'
    success_url = reverse_lazy('semester_list')
    fields = '__all__'


class SemesterUpdateView(UpdateView):
    model = Semester
    template_name = 'edit_semester.html'
    fields = '__all__'
    success_url = reverse_lazy('semester_list')


class SubjectDeleteView(DeleteView):
    model = Subject
    template_name = 'add_subject.html'
    success_url = reverse_lazy('subject_list')
    fields = '__all__'


class SubjectUpdateView(UpdateView):
    model = Subject
    template_name = 'edit_subject.html'
    fields = '__all__'
    success_url = reverse_lazy('subject_list')


class DepartmentListView(ListView):
    model = Department
    template_name = 'department_list.html'
    context_object_name = 'departments'


class SubjectListView(ListView):
    model = Subject
    template_name = 'subject_list.html'
    context_object_name = 'subjects'


class GroupListView(ListView):
    model = Group
    template_name = 'group_list.html'
    context_object_name = 'groups'


class AudienceListView(ListView):
    model = Classroom
    template_name = 'audience_list.html'
    context_object_name = 'audiences'


class DepartmentDeleteView(DeleteView):
    model = Department
    template_name = 'department_confirm_delete.html'
    success_url = reverse_lazy('department_list')


class AddTeacher(CreateView):
    model = Teacher
    template_name = 'add_teacher.html'
    success_url = reverse_lazy('teacher_list')
    fields = '__all__'


class AddLesson(CreateView):
    model = Lesson
    template_name = 'add_lesson.html'
    success_url = reverse_lazy('lesson_list')
    fields = '__all__'

    def form_valid(self, form):
        try:
            form.instance.full_clean()
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)
        return super().form_valid(form)


class AddGroup(CreateView):
    model = Group
    template_name = 'add_group.html'
    success_url = reverse_lazy('group_list')
    fields = '__all__'


class LessonDeleteView(DeleteView):
    model = Lesson
    template_name = 'lesson_confirm_delete.html'
    success_url = reverse_lazy('lesson_list')



class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'group_confirm_delete.html'
    success_url = reverse_lazy('group_list')


class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'edit_group.html'
    fields = '__all__'
    success_url = reverse_lazy('group_list')


class LessonUpdateView(UpdateView):
    model = Lesson
    template_name = 'edit_lesson.html'
    fields = '__all__'
    success_url = reverse_lazy('lesson_list')


class AddAudience(CreateView):
    model = Classroom
    template_name = 'add_audience.html'
    success_url = reverse_lazy('audience_list')
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


class DepartmentUpdateView(UpdateView):
    model = Department
    template_name = 'edit_department.html'
    fields = '__all__'
    success_url = reverse_lazy('department_list')


class TeacherUpdateView(UpdateView):
    model = Teacher
    template_name = 'edit_teacher.html'
    fields = '__all__'
    success_url = reverse_lazy('teacher_list')


class AudienceDeleteView(DeleteView):
    model = Classroom
    template_name = 'audience_confirm_delete.html'
    success_url = reverse_lazy('audience_list')


class AudienceUpdateView(UpdateView):
    model = Classroom
    template_name = 'edit_audience.html'
    fields = '__all__'
    success_url = reverse_lazy('audience_list')


class About(CreateView):
    model = Teacher
    template_name = 'about.html'
    fields = '__all__'


class Contacts(CreateView):
    model = Teacher
    template_name = 'contact.html'
    fields = '__all__'
