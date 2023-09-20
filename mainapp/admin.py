from django.contrib import admin

from mainapp.models import Payments


@admin.register(Payments)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'payment_intent_id',)