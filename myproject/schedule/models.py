from django.db import models


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


class Lesson(models.Model):
    number = models.PositiveIntegerField()
    classroom = models.ForeignKey(Classroom, on_delete=models.PROTECT)
    weekday = models.CharField(max_length=10)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    group = models.CharField(max_length=50)
    course = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    semester = models.ForeignKey(Semester, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Заняття"
        verbose_name_plural = "Заняття"
        ordering = ['weekday', 'number']
        db_table = 'lesson'
        unique_together = ('classroom', 'weekday', 'number')

    def __str__(self):
        return f"{self.subject} ({self.group}) - {self.weekday} пара {self.number}"