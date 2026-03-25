from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=180)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('short_description', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('level', models.CharField(choices=[('beginner', 'Débutant'), ('intermediate', 'Intermédiaire'), ('advanced', 'Avancé')], default='beginner', max_length=20)),
                ('duration_weeks', models.PositiveIntegerField(default=8)),
                ('is_published', models.BooleanField(default=True)),
            ],
            options={'ordering': ['title']},
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.CharField(blank=True, max_length=120)),
                ('job_title', models.CharField(blank=True, max_length=120)),
                ('bio', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=180)),
                ('summary', models.TextField(blank=True)),
                ('order', models.PositiveIntegerField(default=1)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='academy.course')),
            ],
            options={'ordering': ['course', 'order', 'id'], 'unique_together': {('course', 'order')}},
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=180)),
                ('slug', models.SlugField(max_length=200)),
                ('content', models.TextField()),
                ('video_url', models.URLField(blank=True)),
                ('duration_minutes', models.PositiveIntegerField(default=15)),
                ('order', models.PositiveIntegerField(default=1)),
                ('is_preview', models.BooleanField(default=False)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='academy.module')),
            ],
            options={'ordering': ['module', 'order', 'id'], 'unique_together': {('module', 'order'), ('module', 'slug')}},
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['slug'], name='academy_cou_slug_1586b0_idx'),
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('active', 'Actif'), ('completed', 'Terminé'), ('paused', 'En pause')], default='active', max_length=20)),
                ('enrolled_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='academy.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-enrolled_at'], 'unique_together': {('user', 'course')}},
        ),
        migrations.CreateModel(
            name='LessonProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('completed', models.BooleanField(default=False)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_progress', to='academy.enrollment')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress_records', to='academy.lesson')),
            ],
            options={'ordering': ['lesson__module__order', 'lesson__order'], 'unique_together': {('enrollment', 'lesson')}},
        ),
    ]
