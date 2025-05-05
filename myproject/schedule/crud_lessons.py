from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .forms import ScheduleEntryForm
from .models import ScheduleEntry


@require_POST
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    lesson.delete()
    return redirect('schedule_view')


def edit_lesson_view(request, entry_id):
    entry = get_object_or_404(ScheduleEntry, id=entry_id)
    lesson = entry.lesson


    if request.method == 'POST':
        form = ScheduleEntryForm(request.POST)

        if form.is_valid():
            teacher = form.cleaned_data['teacher']
            classroom = form.cleaned_data['classroom']
            day_of_week = form.cleaned_data['day_of_week']
            lesson_number = form.cleaned_data['lesson_number']
            group = form.cleaned_data['group']
            semester = form.cleaned_data['semester']
            course = form.cleaned_data['course']

            teacher_conflict = ScheduleEntry.objects.filter(
                lesson__teacher=teacher,
                day_of_week=day_of_week,
                lesson_number=lesson_number,
                lesson__semester=semester,
            ).exclude(id=entry_id).exists()

            if teacher_conflict:
                form.add_error('teacher', 'Викладач зайнятий у цей день і пару.')

            classroom_conflict = ScheduleEntry.objects.filter(
                classroom=classroom,
                day_of_week=day_of_week,
                lesson_number=lesson_number,
                lesson__semester=semester,
            ).exclude(id=entry_id).exists()

            if classroom_conflict:
                form.add_error('classroom', 'Аудиторія зайнята у цей день і пару.')

            group_conflict = ScheduleEntry.objects.filter(
                group=group,
                day_of_week=day_of_week,
                lesson_number=lesson_number,
                lesson__semester=semester,
            ).exclude(id=entry_id).exists()

            if group_conflict:
                form.add_error('group', 'У групи вже є пара в цей день і пару.')

            if not form.errors and course not in [None, '']:
                lesson.subject = form.cleaned_data['subject']
                lesson.teacher = teacher
                lesson.course = course
                lesson.lesson_type = form.cleaned_data['lesson_type']
                lesson.group = group
                lesson.semester = semester
                lesson.classroom = classroom
                lesson.start_date = form.cleaned_data['start_date']
                lesson.end_date = form.cleaned_data['end_date']
                lesson.save()

                entry.group = group
                entry.classroom = classroom
                entry.day_of_week = day_of_week
                entry.lesson_number = lesson_number
                entry.save()

                return redirect('schedule_view')

            elif course in [None, '']:
                form.add_error('course', 'Поле "Курс" є обов’язковим.')

    else:
        form = ScheduleEntryForm(initial={
            'subject': lesson.subject,
            'teacher': lesson.teacher,
            'course': lesson.course,
            'lesson_type': lesson.lesson_type,
            'group': lesson.group,
            'semester': lesson.semester,
            'classroom': lesson.classroom,
            'start_date': lesson.start_date,
            'end_date': lesson.end_date,
            'day_of_week': entry.day_of_week,
            'lesson_number': entry.lesson_number,
        })

    return render(request, 'schedule/edit_lesson_entry.html', {'form': form, 'entry_id': entry_id})


def add_lesson_view(request):
    if request.method == 'POST':
        form = ScheduleEntryForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data.get('course')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

            teacher = form.cleaned_data['teacher']
            classroom = form.cleaned_data['classroom']
            day_of_week = form.cleaned_data['day_of_week']
            lesson_number = form.cleaned_data['lesson_number']
            group = form.cleaned_data['group']
            semester = form.cleaned_data['semester']

            teacher_conflict = ScheduleEntry.objects.filter(
                lesson__teacher=teacher,
                day_of_week=day_of_week,
                lesson_number=lesson_number,
                lesson__semester=semester,
            ).exists()

            if teacher_conflict:
                form.add_error('teacher',
                               'Викладач зайнятий у цей день і пару.')

            classroom_conflict = ScheduleEntry.objects.filter(
                classroom=classroom,
                day_of_week=day_of_week,
                lesson_number=lesson_number,
                lesson__semester=semester,
            ).exists()

            if classroom_conflict:
                form.add_error('classroom',
                               'Аудиторія зайнята у цей день і пару.')

            group_conflict = ScheduleEntry.objects.filter(
                group=group,
                day_of_week=day_of_week,
                lesson_number=lesson_number,
                lesson__semester=semester,
            ).exists()

            if group_conflict:
                form.add_error('group', 'У групи вже є пара в цей день і пару.')

            if not form.errors and course not in [None, '']:
                lesson, _ = Lesson.objects.get_or_create(
                    subject=form.cleaned_data['subject'],
                    teacher=teacher,
                    course=course,
                    start_date=start_date,
                    end_date=end_date,
                    lesson_type=form.cleaned_data['lesson_type'],
                    group=group,
                    semester=semester,
                    classroom=classroom,
                )
                ScheduleEntry.objects.get_or_create(
                    lesson=lesson,
                    group=group,
                    classroom=classroom,
                    day_of_week=day_of_week,
                    lesson_number=lesson_number,
                )
                return redirect('schedule_view')

            elif course in [None, '']:
                form.add_error('course', 'Поле "Курс" є обов’язковим.')

    else:
        form = ScheduleEntryForm()

    return render(request, 'schedule/add_lesson_entry.html', {'form': form})