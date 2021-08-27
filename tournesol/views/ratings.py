"""
API endpoint to manipulate contributor ratings
"""

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from ..models import ContributorRating, Video
from serializers import ContributorRatingSerializer

class VideoViewSet(viewsets.ModelViewSet):

    queryset = ContributorRating.objects.all()
    serializer_class = ContributorRatingSerializer

    def retrieve(self, pk):
        """
        Get video details and criteria that are related to it
        """

        video = get_object_or_404(Video, video_id=pk)
        ratings = get_object_or_404(ContributorRating, video=video)
        ratings_serialized = ContributorRatingSerializer(ratings)
        return Response(ratings_serialized.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        self.queryset.filter()
        ratings_serialized = ContributorRatingSerializer(self.queryset, many=True)
        return Response(ratings_serialized.data, status=status.HTTP_200_OK)
    
    def update(self, request):
        return Response('Fobidden', status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request):
        return Response('Fobidden', status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        return Response('Fobidden', status=status.HTTP_400_BAD_REQUEST)