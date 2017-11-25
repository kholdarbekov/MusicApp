from django.shortcuts import render, render_to_response
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Chart
from music.models import Music

# Create your views here.


@login_required
def update_charts(request):
    music_pk = request.POST.get('music_pk')
    if music_pk:
        try:
            music = Music.objects.get(pk=music_pk)

            try:
                d_chart = Chart.objects.get(music=music)
                d_chart.num_of_views += 1
                d_chart.save()
                try:
                    up_chart = Chart.objects.get(d_chart.position - 1)
                    if up_chart.num_of_views < d_chart.num_of_views:
                        d_chart.position -= 1
                        up_chart.position += 1
                        d_chart.save()
                        up_chart.save()
                except Chart.DoesNotExist or Chart.MultipleObjectsReturned:
                    pass

            except Chart.DoesNotExist:
                pass

            return JsonResponse({'status': 'ok'})
        except Music.DoesNotExist:
            pass

    else:
        return JsonResponse({'status': 'ko'})


def page_not_found_view(request):
    response = render_to_response('404.html')
    response.status_code = 404
    return response
