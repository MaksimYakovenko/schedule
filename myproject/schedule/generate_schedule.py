from django.shortcuts import render
import random
from django.urls import reverse_lazy, reverse

from schedule.models import (Department, Teacher, Classroom, Lesson, Group,
                             Subject, Semester, ScheduleEntry)
from django.shortcuts import redirect
from collections import defaultdict
from django.db import models



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
    departments = Department.objects.all()
    teacher_id = request.GET.get('teacher_id')
    semester_id = request.GET.get('semester_id')
    department_id = request.GET.get('department_id')
    course = request.GET.get('course')
    group_id = request.GET.get('group_id')
    week_type = request.GET.get('week_type', 'both')

    schedule_entries = ScheduleEntry.objects.all()

    if semester_id in [None, '', 'None']:
        semester_id = None

    if teacher_id in [None, '', 'None']:
        teacher_id = None

    if group_id in [None, '', 'None']:
        group_id = None

    if teacher_id:
        schedule_entries = schedule_entries.filter(
            lesson__teacher_id=teacher_id)

    if department_id:
        schedule_entries = schedule_entries.filter(
            lesson__teacher__department_id=department_id)

    if semester_id:
        schedule_entries = schedule_entries.filter(
            lesson__semester_id=semester_id)

    if group_id:
        schedule_entries = schedule_entries.filter(
            lesson__group_id=group_id)

    if course:
        schedule_entries = schedule_entries.filter(lesson__course=course)

    if week_type in ['even', 'odd']:
        schedule_entries = schedule_entries.filter(
            models.Q(week_type=week_type) | models.Q(week_type='both')
        )

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
        'departments': departments,
        'schedule_entries': schedule_entries,
        'lesson_times': LESSON_TIMES,
        'teachers': teachers,
        'selected_teacher_id': teacher_id,
        'selected_semester_id': semester_id,
        'selected_group_id': group_id,
        'selected_department_id': department_id,
        'semesters': semesters,
        'schedule_availability': schedule_availability,
        'selected_course': course,
        'selected_week_type': week_type,
    }
    return render(request, 'schedule.html', context)