"""
API endpoint to manipulate contributor ratings
"""

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from ..models import ContributorRating
from serializers import ContributorRatingSerializer

class VideoViewSet(viewsets.ModelViewSet):

    queryset = ContributorRating.objects.all()
    serializer_class = ContributorRatingSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Get video details and criteria that are related to it
        """

        video = get_object_or_404(Video, video_id=request.data.get("video_id", ""))
        video_serialized = VideoSerializer(video)
        video_criterias = VideoCriteriaScore.objects.filter(
            video=video
        )
        criterias_serialized = VideoCriteriaScoreSerializer(video_criterias, many=True)
        return Response(
            (video_serialized.data, criterias_serialized.data),
            status=status.HTTP_200_OK
        )