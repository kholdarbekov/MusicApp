from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework import generics, mixins
from .models import Daily, Weekly, Monthly, Music
from .serializers import DailyChartSerializer, WeeklyChartSerializer, MonthlyChartSerializer

# Create your views here.


@login_required
def update_charts(request):
    music_pk = request.POST.get('music_pk')
    if music_pk:
        try:
            music = Music.objects.get(pk=music_pk)

            try:
                d_chart = Daily.objects.get(music=music)
                d_chart.num_of_views += 1
                d_chart.save()
                try:
                    up_chart = Daily.objects.get(d_chart.position - 1)
                    if up_chart.num_of_views < d_chart.num_of_views:
                        d_chart.position -= 1
                        up_chart.position += 1
                        d_chart.save()
                        up_chart.save()
                except Daily.DoesNotExist or Daily.MultipleObjectsReturned:
                    pass

            except Daily.DoesNotExist:
                pass

            try:
                w_chart = Weekly.objects.get(music=music)
                w_chart.num_of_views += 1
                w_chart.save()
                try:
                    up_chart = Weekly.objects.get(w_chart.position - 1)
                    if up_chart.num_of_views < w_chart.num_of_views:
                        w_chart.position -= 1
                        up_chart.position += 1
                        w_chart.save()
                        up_chart.save()
                except Weekly.DoesNotExist or Weekly.MultipleObjectsReturned:
                    pass
            except Weekly.DoesNotExist:
                pass

            try:
                m_chart = Monthly.objects.get(music=music)
                m_chart.num_of_views += 1
                m_chart.save()
                try:
                    up_chart = Monthly.objects.get(m_chart.position - 1)
                    if up_chart.num_of_views < m_chart.num_of_views:
                        m_chart.position -= 1
                        up_chart.position += 1
                        m_chart.save()
                        up_chart.save()
                except Monthly.DoesNotExist or Monthly.MultipleObjectsReturned:
                    pass
            except Monthly.DoesNotExist:
                pass

            return JsonResponse({'status': 'ok'})
        except Music.DoesNotExist:
            pass

    else:
        return JsonResponse({'status': 'ko'})


class DailyChartView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Daily.objects.all()
    serializer_class = DailyChartSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

