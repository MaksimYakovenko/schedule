from django.contrib import admin
from .models import Semester, Department, Teacher, Classroom, Lesson


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('year', 'number', 'start_date', 'end_date')
    list_filter = ('year', 'number')
    search_fields = ('year',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty', 'is_active')
    list_filter = ('faculty', 'is_active')
    search_fields = ('name', 'faculty')
    actions = ['deactivate_departments']

    @admin.action(description="Деактивувати обрані кафедри")
    def deactivate_departments(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'degree', 'department', 'is_active')
    list_filter = ('position', 'degree', 'department', 'is_active')
    search_fields = ('full_name', 'position', 'degree')
    actions = ['deactivate_teachers']

    @admin.action(description="Деактивувати обраних викладачів")
    def deactivate_teachers(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    actions = ['deactivate_classrooms']

    @admin.action(description="Деактивувати обрані аудиторії")
    def deactivate_classrooms(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('number', 'classroom', 'weekday', 'teacher', 'group', 'course', 'subject', 'semester')
    list_filter = ('weekday', 'teacher', 'classroom', 'course', 'semester')
    search_fields = ('group', 'subject')
    ordering = ('weekday', 'number')
