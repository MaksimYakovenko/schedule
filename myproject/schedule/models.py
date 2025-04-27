from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Semester(models.Model):
    year = models.CharField(max_length=20)
    number = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        verbose_name = "Семестр"
        verbose_name_plural = "Семестри"
        ordering = ['-year', 'number']
        db_table = 'semester'

    def __str__(self):
        return f"{self.year} {self.number}"


class Department(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Кафедра"
        verbose_name_plural = "Кафедри"
        ordering = ['name']
        db_table = 'department'

    def __str__(self):
        return self.name


class Teacher(models.Model):
    full_name = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    degree = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Викладач"
        verbose_name_plural = "Викладачі"
        ordering = ['full_name']
        db_table = 'teacher'

    def __str__(self):
        return self.full_name


class Classroom(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Аудиторія"
        verbose_name_plural = "Аудиторії"
        ordering = ['name']
        db_table = 'classroom'

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Група"
        verbose_name_plural = "Групи"
        ordering = ['name']
        db_table = 'group'

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предмети"
        ordering = ['name']
        db_table = 'subject'

    def __str__(self):
        return self.name


class Lesson(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    course = models.CharField(max_length=1, choices=[(str(i), f"{i} курс") for i in range(1, 7)])
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    semester = models.ForeignKey(Semester, on_delete=models.PROTECT)
    hours_per_week = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Кількість пар на тиждень"
    )

    class Meta:
        verbose_name = "Заняття"
        verbose_name_plural = "Заняття"
        db_table = 'lesson'

    def __str__(self):
        return f"{self.subject} ({self.group})"



class ScheduleEntry(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    day_of_week = models.CharField(
        max_length=10,
        choices=[
            ('Понеділок', 'Понеділок'),
            ('Вівторок', 'Вівторок'),
            ('Середа', 'Середа'),
            ('Четвер', 'Четвер'),
            ('Пʼятниця', 'Пʼятниця')
        ],
        default='Понеділок'
    )
    lesson_number = models.PositiveIntegerField(null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = "Розклад"
        verbose_name_plural = "Розклади"
        db_table = 'schedule_entry'

    def __str__(self):
        return f"{self.group} - {self.day_of_week} пара {self.lesson_number}"

