from rest_framework import generics
from ..models import Chart
from .serializers import DailyChartSerializer


class DailyChartView(generics.ListAPIView):
    queryset = Chart.objects.all()
    serializer_class = DailyChartSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

