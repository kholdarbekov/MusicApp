from django.contrib import admin
from .models import Daily, Weekly, Monthly
# Register your models here.


@admin.register(Daily)
class DailyChartAdmin(admin.ModelAdmin):
    list_display = ['music', 'position']
    readonly_fields = ['num_of_views']


@admin.register(Weekly)
class WeeklyChartAdmin(admin.ModelAdmin):
    list_display = ['music', 'position']
    readonly_fields = ['num_of_views']


@admin.register(Monthly)
class MonthlyChartAdmin(admin.ModelAdmin):
    list_display = ['music', 'position']
    readonly_fields = ['num_of_views']
