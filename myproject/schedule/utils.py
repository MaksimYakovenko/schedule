import random
from collections import defaultdict

def generate_schedule(semester):
    days = ['mon', 'tue', 'wed', 'thu', 'fri']
    time_slots = [1, 2, 3, 4]

    schedule = defaultdict(lambda: defaultdict(lambda: {'group': set(), 'teacher': set(), 'classroom': set()}))
    classrooms = list(Classroom.objects.filter(is_active=True))
    lessons = Lesson.objects.filter(semester=semester)

    ScheduleEntry.objects.filter(lesson__semester=semester).delete()

    for lesson in lessons:
        hours_left = lesson.hours_per_week

        while hours_left > 0:
            day = random.choice(days)
            time = random.choice(time_slots)
            available_classrooms = [c for c in classrooms
                if c.id not in schedule[day][time]['classroom']]

            if (lesson.group.id in schedule[day][time]['group'] or
                lesson.teacher.id in schedule[day][time]['teacher'] or
                not available_classrooms):
                continue

            classroom = random.choice(available_classrooms)
            ScheduleEntry.objects.create(
                lesson=lesson,
                day=day,
                time_slot=time,
                classroom=classroom
            )

            schedule[day][time]['group'].add(lesson.group.id)
            schedule[day][time]['teacher'].add(lesson.teacher.id)
            schedule[day][time]['classroom'].add(classroom.id)

            hours_left -= 1
