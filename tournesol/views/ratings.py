"""
API endpoint to manipulate contributor ratings
"""

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from ..models import ContributorRating, Video
from serializers import ContributorRatingSerializer


def verify_username(request, username):
    """ Fails if username is different from request.user """
    if request.user.username != username:
        raise PermissionDenied("403 Forbidden")


class ContributorRatingViewSet(viewsets.ModelViewSet):

    queryset = ContributorRating.objects.all()
    serializer_class = ContributorRatingSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Get video details and criteria that are related to it
        """

        verify_username(request, kwargs["username"])
        video = get_object_or_404(Video, video_id=kwargs["video_id"])
        ratings = get_object_or_404(ContributorRating, video=video, user=request.user)
        ratings_serialized = ContributorRatingSerializer(ratings)
        return Response(ratings_serialized.data, status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):

        verify_username(request, kwargs["username"])
        self.queryset.filter(user=request.user)
        ratings_serialized = ContributorRatingSerializer(self.queryset, many=True)
        return Response(ratings_serialized.data, status=status.HTTP_200_OK)
    
    def update(self, request):
        return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)
    
    def create(self, request):
        return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request):
        return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)