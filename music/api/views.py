from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Playlist
from .serializers import PlaylistSerializers


class PlayListCreate(APIView):
    http_method_names = ['post', ]
    parser_classes = (FormParser, MultiPartParser)

    def post(self, request):
        serializer = PlaylistSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

