"""
API endpoint to manipulate contributor ratings
"""

from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from ..models import ContributorRating, Video
from ..serializers import ContributorRatingSerializer


def verify_username(request, username):
    """ Fails if username is different from request.user """
    if request.user.username != username:
        raise PermissionDenied("403 Forbidden")


class ContributorRatingDetail(
    mixins.ListModelMixin, generics.GenericAPIView
):

    queryset = ContributorRating.objects.all()
    serializer_class = ContributorRatingSerializer

    def get(self, request, *args, **kwargs):
        """
        Get video details and criteria that are related to it
        """

        verify_username(request, kwargs["username"])
        video = get_object_or_404(Video, video_id=kwargs["video_id"])
        ratings = get_object_or_404(ContributorRating, video=video, user=request.user)
        ratings_serialized = ContributorRatingSerializer(ratings)
        return Response(ratings_serialized.data, status=status.HTTP_200_OK)


class ContributorRatingList(
    mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):

    def get(self, request, *args, **kwargs):

        verify_username(request, kwargs["username"])
        self.queryset.filter(user=request.user)
        ratings_serialized = ContributorRatingSerializer(self.queryset, many=True)
        return Response(ratings_serialized.data, status=status.HTTP_200_OK)
