from django.contrib import admin

from .models import Course, Enrollment, Lesson, LessonProgress, Module, StudentProfile


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'duration_weeks', 'is_published')
    list_filter = ('level', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'short_description')
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'summary')
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order', 'duration_minutes', 'is_preview')
    list_filter = ('module__course', 'is_preview')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'status', 'enrolled_at')
    list_filter = ('status', 'course')
    search_fields = ('user__username', 'user__email', 'course__title')


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'lesson', 'completed', 'completed_at')
    list_filter = ('completed', 'lesson__module__course')
    search_fields = ('enrollment__user__username', 'lesson__title')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'job_title')
    search_fields = ('user__username', 'user__email', 'country', 'job_title')
