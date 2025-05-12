from django.shortcuts import render, redirect
import random
from django.urls import reverse_lazy, reverse

from schedule.models import (Department, Teacher, Classroom, Lesson, Group,
                             Subject, Semester, ScheduleEntry, Session,
                             SessionEntry)
from collections import defaultdict
from django.db import models
from .forms import GenerateSessionForm
from django.contrib import messages



DAYS_OF_WEEK = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'Пʼятниця',
                'Субота']
LESSON_NUMBERS = [1, 2, 3, 4]


def generate_session_schedule(semester):
    sessions = Session.objects.filter(semester=semester)
    used_slots = set()

    SessionEntry.objects.filter(semester=semester).delete()

    for session in sessions:
        random_days = DAYS_OF_WEEK[:]
        random.shuffle(random_days)

        random_lesson_numbers = LESSON_NUMBERS[:]
        random.shuffle(random_lesson_numbers)

        placed = False
        for day in random_days:
            for number in random_lesson_numbers:
                key = (day, number, session.classroom_id, session.group_id)
                if key not in used_slots:
                    used_slots.add(key)
                    SessionEntry.objects.create(
                        group=session.group,
                        day_of_week=day,
                        lesson_number=number,
                        session=session,
                        classroom=session.classroom,
                        semester=session.semester
                    )
                    placed = True
                    break
            if placed:
                break


def generate_session_view(request):
    session_entries_by_course = defaultdict(list)

    if request.method == 'POST':
        form = GenerateSessionForm(request.POST)
        if form.is_valid():
            semester = form.cleaned_data['semester']
            generate_session_schedule(semester)
            messages.success(request, f'Сесію для семестру "{semester}" згенеровано!')

            session_entries = SessionEntry.objects.filter(
                semester=semester
            ).select_related('group', 'session', 'classroom')

            for entry in session_entries:
                session_entries_by_course[entry.session.course].append(entry)
    else:
        form = GenerateSessionForm()

    return render(request, 'generate_session.html', {
        'form': form,
        'session_entries_by_course': dict(session_entries_by_course),
    })