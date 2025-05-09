from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, ValidationError


class Semester(models.Model):
    year = models.CharField(max_length=20, verbose_name='Навчальний рік')
    number = models.CharField(max_length=10, verbose_name='Номер семестру')
    start_date = models.DateField(verbose_name='Дата початку')
    end_date = models.DateField(verbose_name='Дата закінчення')

    class Meta:
        verbose_name = "Семестр"
        verbose_name_plural = "Семестри"
        ordering = ['-year', 'number']
        db_table = 'semester'

    def __str__(self):
        return f"{self.year} {self.number}"


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name='Назва кафедри')
    faculty = models.CharField(max_length=100, verbose_name='Факультет')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Кафедра"
        verbose_name_plural = "Кафедри"
        ordering = ['name']
        db_table = 'department'

    def __str__(self):
        return self.name


class Teacher(models.Model):
    full_name = models.CharField(max_length=200, verbose_name='ПІБ')
    position = models.CharField(max_length=100, verbose_name='Посада')
    degree = models.CharField(max_length=100, blank=True, null=True,
                              verbose_name='Науковий ступінь')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   verbose_name='Належність до кафедри')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Викладач"
        verbose_name_plural = "Викладачі"
        ordering = ['full_name']
        db_table = 'teacher'

    def __str__(self):
        return self.full_name


class Classroom(models.Model):
    name = models.CharField(max_length=50, verbose_name='Номер')
    capacity = models.PositiveIntegerField(verbose_name='Місткість')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Аудиторія"
        verbose_name_plural = "Аудиторії"
        ordering = ['name']
        db_table = 'classroom'

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name='Назва групи')

    class Meta:
        verbose_name = "Група"
        verbose_name_plural = "Групи"
        ordering = ['name']
        db_table = 'group'

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва предмету')

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предмети"
        ordering = ['name']
        db_table = 'subject'

    def __str__(self):
        return self.name


class Lesson(models.Model):
    PRACTICAL = 'Практична'
    LECTURE = 'Лекція'
    SEMINAR = 'Семінар'
    LABORATORY = 'Лабораторна'
    CONSULTATION = 'Консультація'

    LESSON_TYPE_CHOICES = [
        (PRACTICAL, 'Практична'),
        (LECTURE, 'Лекція'),
        (SEMINAR, 'Семінар'),
        (LABORATORY, 'Лабораторна'),
        (CONSULTATION, 'Консультація'),
    ]


    COURSE_CHOICES = [
        ('1', '1 курс'),
        ('2', '2 курс'),
        ('3', '3 курс'),
        ('4', '4 курс'),
        ('m1', '1 курс маг.'),
        ('m2', '2 курс маг.'),
    ]

    WEEK_CHOICES = [
        ('even', 'Парний тиждень'),
        ('odd', 'Непарний тиждень'),
        ('both', 'Щотижня'),
    ]

    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT,
                                verbose_name='Викладач')
    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                              verbose_name='Група')
    course = models.CharField(max_length=2, choices=COURSE_CHOICES,
                              null=False, blank=False, verbose_name='Курс')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT,
                                verbose_name='Предмет')
    semester = models.ForeignKey(Semester, on_delete=models.PROTECT,
                                 verbose_name='Семестр')
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Аудиторія'
    )
    hours_per_week = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Кількість пар на тиждень"
    )

    lesson_type = models.CharField(
        max_length=20,
        choices=LESSON_TYPE_CHOICES,
        default=PRACTICAL,
        verbose_name="Тип заняття"
    )

    start_date = models.DateField(
        verbose_name="Дата початку",
        null=True,
        blank=True
    )

    end_date = models.DateField(
        verbose_name="Дата завершення",
        null=True,
        blank=True
    )

    week_type = models.CharField(max_length=5, choices=WEEK_CHOICES,
                                 default='both')

    def clean(self):
        super().clean()

        if self.start_date and self.end_date and self.semester:
            if self.start_date < self.semester.start_date:
                raise ValidationError({
                    'start_date': (
                        'Дата початку заняття не може бути раніше початку семестру.')
                })
            if self.end_date > self.semester.end_date:
                raise ValidationError({
                    'end_date': (
                        'Дата завершення заняття не може бути пізніше закінчення семестру.')
                })
            if self.start_date > self.end_date:
                raise ValidationError(
                    'Дата початку заняття не може бути пізніше дати завершення.')

    class Meta:
        verbose_name = "Заняття"
        verbose_name_plural = "Заняття"
        db_table = 'lesson'

    def __str__(self):
        return f"{self.subject} ({self.group}) -\
                {self.lesson_type}"



class ScheduleEntry(models.Model):
    WEEK_TYPE_CHOICES = [
        ('even', 'Парний'),
        ('odd', 'Непарний'),
        ('both', 'Щотижня'),
    ]

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
    semester = models.ForeignKey(Semester, on_delete=models.PROTECT, null=True,
                                 blank=True)
    week_type = models.CharField(
        max_length=10,
        choices=WEEK_TYPE_CHOICES,
        default='both'
    )

    class Meta:
        verbose_name = "Розклад"
        verbose_name_plural = "Розклади"
        db_table = 'schedule_entry'

    def __str__(self):
        return f"{self.group} - {self.day_of_week} пара {self.lesson_number}"

