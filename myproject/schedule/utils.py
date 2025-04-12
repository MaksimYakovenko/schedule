# utils.py (або файл, де визначена генерація розкладу)
from schedule.models import ScheduleEntry, Lesson, TimeSlot, Classroom

def generate_schedule():
    lessons = Lesson.objects.all()
    timeslots = Timeslot.objects.all()
    classrooms = Classroom.objects.all()

    for lesson in lessons:
        for timeslot in timeslots:
            for classroom in classrooms:
                # Створення нового запису для розкладу
                ScheduleEntry.objects.create(
                    lesson=lesson,
                    timeslot=timeslot,
                    classroom=classroom
                )
