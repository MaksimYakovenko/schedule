import random
from schedule.models import Lesson, Subject, Teacher, Classroom


def generate_schedule():
    teachers = list(Teacher.objects.all())
    subjects = list(Subject.objects.all())
    classrooms = list(Classroom.objects.all())
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    times = ['09:00', '11:00', '13:00', '15:00']

    Lesson.objects.all().delete()

    for day in days:
        for time in times:
            if teachers and subjects and classrooms:
                teacher = random.choice(teachers)
                subject = random.choice(subjects)
                classroom = random.choice(classrooms)

                Lesson.objects.create(
                    subject=subject,
                    teacher=teacher,
                    classroom=classroom,
                    day=day,
                    time=time
                )
