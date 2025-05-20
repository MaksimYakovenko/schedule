from django.shortcuts import render
from .models import Lesson, Semester
from django.views.decorators.http import require_http_methods
from django.contrib import messages


@require_http_methods(["GET", "POST"])
def copy_lessons_view(request):
    semesters = Semester.objects.all()
    success = False

    if request.method == "POST":
        source_id = request.POST.get("source_semester")
        target_id = request.POST.get("target_semester")

        if source_id and target_id and source_id != target_id:
            source = Semester.objects.get(id=source_id)
            target = Semester.objects.get(id=target_id)

            lessons = Lesson.objects.filter(semester=source)

            for lesson in lessons:
                Lesson.objects.create(
                    teacher=lesson.teacher,
                    group=lesson.group,
                    course=lesson.course,
                    subject=lesson.subject,
                    semester=target,
                    classroom=lesson.classroom,
                    hours_per_week=lesson.hours_per_week,
                    lesson_type=lesson.lesson_type,
                    start_date=lesson.start_date,
                    end_date=lesson.end_date,
                    week_type=lesson.week_type,
                )

            success = True
        else:
            messages.error(request, "Оберіть різні семестри.")

    return render(request, 'copy_schedule.html', {
        'semesters': semesters,
        'success': success
    })