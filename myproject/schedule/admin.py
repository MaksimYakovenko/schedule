from django.contrib import admin
from schedule.models import (Department, Teacher, Classroom, Lesson, Group,
                             Subject, Semester)



@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('year', 'number', 'start_date', 'end_date')
    list_filter = ('year', 'number')
    search_fields = ('year',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ('name',)


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
    list_display = ('subject', 'group', 'teacher', 'course', 'semester', 'hours_per_week')
    list_filter = ('teacher', 'group', 'course', 'semester')
    search_fields = ('subject__name', 'group__name')
    autocomplete_fields = ('teacher', 'group', 'subject', 'semester')


@admin.action(description='Згенерувати розклад')
def generate_schedule_action(modeladmin, request, queryset):
    for semester in queryset:
        generate_schedule(semester)

class SemesterAdmin(admin.ModelAdmin):
    actions = [generate_schedule_action]

