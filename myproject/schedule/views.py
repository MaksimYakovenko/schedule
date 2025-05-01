from django.shortcuts import render, get_object_or_404
import random
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from schedule.models import (Department, Teacher, Classroom, Lesson, Group,
                             Subject, Semester, ScheduleEntry)
from django.shortcuts import redirect
from collections import defaultdict
from django.views.decorators.http import require_POST


def home(request):
    teacher_count = Teacher.objects.count()
    department_count = Department.objects.count()
    lessons_count = ScheduleEntry.objects.count()
    return render(request, 'home.html', {
        'teacher_count': teacher_count,
        'department_count': department_count,
        'lessons_count': lessons_count
    })



DAYS_OF_WEEK = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'Пʼятниця']
LESSON_NUMBERS = [1, 2, 3, 4]
LESSON_TIMES = {
    1: '08:00-09:00',
    2: '10:00-11:00',
    3: '12:00-13:00',
    4: '14:00-15:00',
}


def generate_schedule(request):
    if request.method == 'POST':
        semester_id = request.POST.get('semester_id')
        if not semester_id:
            return HttpResponseBadRequest("Семестр не вибрано.")

    ScheduleEntry.objects.all().delete()

    groups = Group.objects.filter(lesson__isnull=False).distinct()
    classrooms = Classroom.objects.all()

    teacher_occupancy = defaultdict(set)
    classroom_occupancy = defaultdict(set)
    group_occupancy = defaultdict(set)
    schedule_dict = {}

    for group in groups:
        group_lessons = Lesson.objects.filter(group=group)

        for lesson in group_lessons:
            lessons_scheduled = 0
            attempts = 0
            max_attempts = 100

            while lessons_scheduled < lesson.hours_per_week and attempts < max_attempts:
                attempts += 1
                day = random.choice(DAYS_OF_WEEK)
                lesson_number = random.choice(LESSON_NUMBERS)

                if (
                    lesson.teacher.id in teacher_occupancy[(day, lesson_number)]
                    or group.id in group_occupancy[(day, lesson_number)]
                ):
                    continue

                available_classrooms = [
                    classroom for classroom in classrooms
                    if classroom.id not in classroom_occupancy[(day, lesson_number)]
                ]

                if not available_classrooms:
                    continue

                classroom = random.choice(available_classrooms)

                ScheduleEntry.objects.create(
                    group=group,
                    day_of_week=day,
                    lesson_number=lesson_number,
                    lesson=lesson,
                    classroom=classroom
                )

                teacher_occupancy[(day, lesson_number)].add(lesson.teacher.id)
                classroom_occupancy[(day, lesson_number)].add(classroom.id)
                group_occupancy[(day, lesson_number)].add(group.id)

                if group.id not in schedule_dict:
                    schedule_dict[group.id] = {}
                schedule_dict[group.id].setdefault(day, []).append(lesson_number)

                lessons_scheduled += 1

    request.session['schedule_dict'] = schedule_dict
    return redirect(f"{reverse('schedule_view')}?semester_id={semester_id}")

def schedule_view(request):
    groups = Group.objects.all()
    teachers = Teacher.objects.all()
    semesters = Semester.objects.all()
    teacher_id = request.GET.get('teacher_id')
    semester_id = request.GET.get('semester_id')
    course = request.GET.get('course')

    schedule_entries = ScheduleEntry.objects.all()

    if semester_id in [None, '', 'None']:
        semester_id = None

    if teacher_id in [None, '', 'None']:
        teacher_id = None

    if teacher_id:
        schedule_entries = schedule_entries.filter(
            lesson__teacher_id=teacher_id)

    if semester_id:
        schedule_entries = schedule_entries.filter(
            lesson__semester_id=semester_id)

    if course:
        schedule_entries = schedule_entries.filter(lesson__course=course)


    schedule_entries = sorted(
        schedule_entries,
        key=lambda x: (DAYS_OF_WEEK.index(x.day_of_week), x.lesson_number)
    )

    groups_with_schedule = []

    for group in groups:
        has_lessons = any(entry.group == group for entry in schedule_entries)
        if has_lessons:
            groups_with_schedule.append(group)

    schedule_availability = {}
    for group in groups:
        schedule_availability[group.id] = {}
        for day in DAYS_OF_WEEK:
            schedule_availability[group.id][day] = False

        for entry in schedule_entries:
            if entry.group.id not in schedule_availability:
                schedule_availability[entry.group.id] = {}

            schedule_availability[entry.group.id][entry.day_of_week] = True

    groups_by_course = defaultdict(list)
    for group in groups_with_schedule:
        lessons = Lesson.objects.filter(group=group)
        distinct_courses = lessons.values_list('course', flat=True).distinct()

        for course in distinct_courses:
            groups_by_course[course].append(group)

    sorted_course_keys = sorted(
        groups_by_course.keys(),
        key=lambda x: (int(x[1]) if x.startswith('m') else int(x))
        if x.isdigit() else (5 if x == 'm1' else 6)
    )

    context = {
        'groups_by_course': dict(groups_by_course),
        'sorted_course_keys': sorted_course_keys,
        'groups_with_schedule': groups_with_schedule,
        'days_of_week': DAYS_OF_WEEK,
        'lesson_numbers': LESSON_NUMBERS,
        'groups': groups,
        'schedule_entries': schedule_entries,
        'lesson_times': LESSON_TIMES,
        'teachers': teachers,
        'selected_teacher_id': teacher_id,
        'selected_semester_id': semester_id,
        'semesters': semesters,
        'schedule_availability': schedule_availability,
        'selected_course': course,
    }
    return render(request, 'schedule.html', context)


@require_POST
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    lesson.delete()
    return redirect('schedule_view')


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
