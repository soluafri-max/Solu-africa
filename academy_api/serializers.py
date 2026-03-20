from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Category, Enrollment, Lesson, LessonProgress, Module, Program, Subscription, SubscriptionPlan

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        email = validated_data['email'].lower()
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password'],
        )
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'is_active', 'created_at', 'updated_at']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id',
            'module',
            'title',
            'description',
            'position',
            'video_url',
            'duration_seconds',
            'is_preview',
            'is_published',
            'created_at',
            'updated_at',
        ]


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = [
            'id',
            'program',
            'title',
            'description',
            'position',
            'unlock_delay_days',
            'is_mandatory',
            'requires_previous_module_completion',
            'requires_quiz_pass',
            'minimum_quiz_score',
            'estimated_duration_minutes',
            'is_published',
            'lessons',
            'created_at',
            'updated_at',
        ]


class ProgramSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Program
        fields = [
            'id',
            'category',
            'category_id',
            'title',
            'slug',
            'short_description',
            'description',
            'level',
            'language',
            'thumbnail',
            'trailer_video_url',
            'subscription_required',
            'certificate_enabled',
            'accelerated_unlock_enabled',
            'unlock_interval_days',
            'is_featured',
            'is_published',
            'modules',
            'created_at',
            'updated_at',
        ]


class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    program = ProgramSerializer(read_only=True)
    program_id = serializers.PrimaryKeyRelatedField(queryset=Program.objects.all(), source='program', write_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'program', 'program_id', 'status', 'enrolled_at', 'created_at', 'updated_at']
        read_only_fields = ['status', 'enrolled_at']

    def create(self, validated_data):
        return Enrollment.objects.create(user=self.context['request'].user, **validated_data)


class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = [
            'id',
            'enrollment',
            'lesson',
            'watched_seconds',
            'last_position_seconds',
            'completion_percent',
            'is_completed',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['enrollment', 'lesson']


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'code', 'amount', 'currency', 'interval', 'trial_days', 'is_active', 'created_at', 'updated_at']


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer(read_only=True)
    plan_id = serializers.PrimaryKeyRelatedField(queryset=SubscriptionPlan.objects.all(), source='plan', write_only=True)

    class Meta:
        model = Subscription
        fields = [
            'id',
            'plan',
            'plan_id',
            'status',
            'started_at',
            'current_period_end',
            'provider',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['status', 'started_at']

    def create(self, validated_data):
        return Subscription.objects.create(user=self.context['request'].user, **validated_data)
