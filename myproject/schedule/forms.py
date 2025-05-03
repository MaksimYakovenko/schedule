from django import forms
from .models import Lesson, Group, Classroom, Semester

DAYS_OF_WEEK = [
    ('Понеділок', 'Понеділок'),
    ('Вівторок', 'Вівторок'),
    ('Середа', 'Середа'),
    ('Четвер', 'Четвер'),
    ('Пʼятниця', 'Пʼятниця'),
]

class LessonForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    classroom = forms.ModelChoiceField(queryset=Classroom.objects.all())
    semester = forms.ModelChoiceField(queryset=Semester.objects.all())
    day_of_week = forms.ChoiceField(choices=DAYS_OF_WEEK)
    lesson_number = forms.IntegerField(min_value=1, max_value=4)

    class Meta:
        model = Lesson
        fields = ['subject', 'teacher', 'lesson_type']


class EditLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['subject', 'teacher', 'lesson_type', 'start_date', 'end_date']
