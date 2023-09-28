from django.contrib import admin

from mainapp.models import Payments, Course


@admin.register(Payments)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'payment_intent_id',)
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title',)