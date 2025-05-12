from random import choices

from django import forms
from .models import Lesson, Group, Classroom, Semester, Subject, Teacher

DAYS_OF_WEEK = [
    ('Понеділок', 'Понеділок'),
    ('Вівторок', 'Вівторок'),
    ('Середа', 'Середа'),
    ('Четвер', 'Четвер'),
    ('Пʼятниця', 'Пʼятниця'),
]

LESSON_TYPE_CHOICES = [
    ('Практична', 'Практична'),
    ('Лекція', 'Лекція'),
    ('Семінар', 'Семінар'),
    ('Лабараторна', 'Лабораторна'),
    ('Консультація', 'Консультація'),
]

LESSON_NUMBERS = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
]


class ScheduleEntryForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())
    course = forms.ChoiceField(choices=Lesson.COURSE_CHOICES)
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)
    lesson_type = forms.ChoiceField(choices=LESSON_TYPE_CHOICES)
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    classroom = forms.ModelChoiceField(queryset=Classroom.objects.all())
    semester = forms.ModelChoiceField(queryset=Semester.objects.all())
    day_of_week = forms.ChoiceField(choices=DAYS_OF_WEEK)
    lesson_number = forms.ChoiceField(choices=LESSON_NUMBERS)


class GenerateSessionForm(forms.Form):
    semester = forms.ModelChoiceField(
        queryset=Semester.objects.all(),
        label='Оберіть семестр',
        required=True
    )
