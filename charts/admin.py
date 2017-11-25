from django.contrib import admin
from .models import Chart, MusicInChart
from .forms import ChartForm
# Register your models here.


@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    form = ChartForm
    filter_horizontal = ['musics']


@admin.register(MusicInChart)
class MusicInChartAdmin(admin.ModelAdmin):
    pass

