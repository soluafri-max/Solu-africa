from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StudentProfile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    country = models.CharField(max_length=120, blank=True)
    job_title = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self) -> str:
        return f'Profil de {self.user.username}'


class Course(TimeStampedModel):
    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    ADVANCED = 'advanced'
    LEVEL_CHOICES = [
        (BEGINNER, 'Débutant'),
        (INTERMEDIATE, 'Intermédiaire'),
        (ADVANCED, 'Avancé'),
    ]

    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True, max_length=200)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default=BEGINNER)
    duration_weeks = models.PositiveIntegerField(default=8)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['title']

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def total_lessons(self) -> int:
        return Lesson.objects.filter(module__course=self).count()


class Module(TimeStampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=180)
    summary = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['course', 'order', 'id']
        unique_together = [('course', 'order')]

    def __str__(self) -> str:
        return f'{self.course.title} · {self.title}'


class Lesson(TimeStampedModel):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200)
    content = models.TextField()
    video_url = models.URLField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=15)
    order = models.PositiveIntegerField(default=1)
    is_preview = models.BooleanField(default=False)

    class Meta:
        ordering = ['module', 'order', 'id']
        unique_together = [('module', 'order'), ('module', 'slug')]

    def __str__(self) -> str:
        return f'{self.module.title} · {self.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Enrollment(TimeStampedModel):
    ACTIVE = 'active'
    COMPLETED = 'completed'
    PAUSED = 'paused'
    STATUS_CHOICES = [
        (ACTIVE, 'Actif'),
        (COMPLETED, 'Terminé'),
        (PAUSED, 'En pause'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE)
    enrolled_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-enrolled_at']
        unique_together = [('user', 'course')]

    def __str__(self) -> str:
        return f'{self.user.username} → {self.course.title}'

    @property
    def completed_lessons(self) -> int:
        return self.lesson_progress.filter(completed=True).count()

    @property
    def progress_percent(self) -> int:
        total_lessons = self.course.total_lessons
        if total_lessons == 0:
            return 0
        return int((self.completed_lessons / total_lessons) * 100)


class LessonProgress(TimeStampedModel):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress_records')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['lesson__module__order', 'lesson__order']
        unique_together = [('enrollment', 'lesson')]

    def __str__(self) -> str:
        return f'{self.enrollment} · {self.lesson.title}'

    def mark_completed(self):
        self.completed = True
        self.completed_at = timezone.now()
        self.save(update_fields=['completed', 'completed_at', 'updated_at'])
