from django.contrib import admin

from .models import Category, Enrollment, Lesson, LessonProgress, Module, Program, Subscription, SubscriptionPlan

admin.site.register(Category)
admin.site.register(Program)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(LessonProgress)
admin.site.register(SubscriptionPlan)
admin.site.register(Subscription)
