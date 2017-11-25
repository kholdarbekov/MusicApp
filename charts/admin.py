from django.contrib import admin
from .models import Chart, MusicInChart
# Register your models here.


@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    filter_horizontal = ['musics']


@admin.register(MusicInChart)
class MusicInChartAdmin(admin.ModelAdmin):
    pass

