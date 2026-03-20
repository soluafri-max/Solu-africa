from datetime import timedelta

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimestampedModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Program(TimestampedModel):
    LEVEL_BEGINNER = 'beginner'
    LEVEL_INTERMEDIATE = 'intermediate'
    LEVEL_ADVANCED = 'advanced'
    LEVEL_CHOICES = [
        (LEVEL_BEGINNER, 'Beginner'),
        (LEVEL_INTERMEDIATE, 'Intermediate'),
        (LEVEL_ADVANCED, 'Advanced'),
    ]

    category = models.ForeignKey(Category, related_name='programs', on_delete=models.PROTECT)
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default=LEVEL_BEGINNER)
    language = models.CharField(max_length=10, default='fr')
    thumbnail = models.URLField(blank=True)
    trailer_video_url = models.URLField(blank=True)
    subscription_required = models.BooleanField(default=True)
    certificate_enabled = models.BooleanField(default=True)
    accelerated_unlock_enabled = models.BooleanField(default=False)
    unlock_interval_days = models.PositiveSmallIntegerField(default=30)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Module(TimestampedModel):
    program = models.ForeignKey(Program, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    position = models.PositiveIntegerField(default=1)
    unlock_delay_days = models.PositiveSmallIntegerField(default=0)
    is_mandatory = models.BooleanField(default=True)
    requires_previous_module_completion = models.BooleanField(default=False)
    requires_quiz_pass = models.BooleanField(default=False)
    minimum_quiz_score = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    estimated_duration_minutes = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['program', 'position']
        unique_together = [('program', 'position')]

    def __str__(self):
        return f'{self.program.title} - {self.title}'


class Lesson(TimestampedModel):
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    position = models.PositiveIntegerField(default=1)
    video_url = models.URLField(blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    is_preview = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['module', 'position']
        unique_together = [('module', 'position')]

    def __str__(self):
        return f'{self.module.title} - {self.title}'


class Enrollment(TimestampedModel):
    STATUS_ACTIVE = 'active'
    STATUS_COMPLETED = 'completed'
    STATUS_SUSPENDED = 'suspended'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_SUSPENDED, 'Suspended'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='enrollments', on_delete=models.CASCADE)
    program = models.ForeignKey(Program, related_name='enrollments', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    enrolled_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-enrolled_at']
        unique_together = [('user', 'program')]

    def __str__(self):
        return f'{self.user} -> {self.program}'

    def module_unlock_status(self):
        modules = list(self.program.modules.order_by('position'))
        interval = 15 if self.program.accelerated_unlock_enabled else self.program.unlock_interval_days
        status_payload = []
        for index, module in enumerate(modules):
            unlock_at = self.enrolled_at + timedelta(days=index * interval)
            status_payload.append(
                {
                    'module_id': module.id,
                    'title': module.title,
                    'position': module.position,
                    'is_unlocked': timezone.now() >= unlock_at,
                    'unlocked_at': unlock_at if timezone.now() >= unlock_at else None,
                    'next_unlock_at': None if timezone.now() >= unlock_at else unlock_at,
                }
            )
        return status_payload


class LessonProgress(TimestampedModel):
    enrollment = models.ForeignKey(Enrollment, related_name='lesson_progress', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='progress_entries', on_delete=models.CASCADE)
    watched_seconds = models.PositiveIntegerField(default=0)
    last_position_seconds = models.PositiveIntegerField(default=0)
    completion_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = [('enrollment', 'lesson')]

    def __str__(self):
        return f'{self.enrollment} - {self.lesson}'


class SubscriptionPlan(TimestampedModel):
    INTERVAL_MONTH = 'month'
    INTERVAL_YEAR = 'year'
    INTERVAL_CHOICES = [
        (INTERVAL_MONTH, 'Month'),
        (INTERVAL_YEAR, 'Year'),
    ]

    name = models.CharField(max_length=120)
    code = models.SlugField(max_length=120, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    interval = models.CharField(max_length=10, choices=INTERVAL_CHOICES, default=INTERVAL_MONTH)
    trial_days = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['amount']

    def __str__(self):
        return self.name


class Subscription(TimestampedModel):
    STATUS_ACTIVE = 'active'
    STATUS_TRIALING = 'trialing'
    STATUS_GRACE = 'grace_period'
    STATUS_CANCELLED = 'cancelled'
    STATUS_EXPIRED = 'expired'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_TRIALING, 'Trialing'),
        (STATUS_GRACE, 'Grace period'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_EXPIRED, 'Expired'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subscriptions', on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, related_name='subscriptions', on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    started_at = models.DateTimeField(default=timezone.now)
    current_period_end = models.DateTimeField(null=True, blank=True)
    provider = models.CharField(max_length=30, default='manual')

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f'{self.user} - {self.plan}'
