from rest_framework import generics
from ..models import Chart
from .serializers import ChartSerializer


class ChartView(generics.ListAPIView):
    queryset = Chart.objects.all()
    serializer_class = ChartSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

