# coding: utf-8

"""
Defines Tournesol's backend API routes
"""

from django.urls import include, path
from rest_framework import routers

from tournesol.views.video_rate_later import VideoRateLaterDetail, VideoRateLaterList
from tournesol.views.video import VideoViewSet
from tournesol.views.ratings import ContributorRatingList, ContributorRatingDetail

from .views import ComparisonViewSet

router = routers.DefaultRouter()
router.register(r"comparison", ComparisonViewSet)
router.register(r'video', VideoViewSet)


app_name = "tournesol"
urlpatterns = [
    path("", include(router.urls)),
    # VideoRateLater API
    path(
        "users/<str:username>/video_rate_later/",
        VideoRateLaterList.as_view(),
        name="video_rate_later_list",
    ),
    path(
        "users/<str:username>/video_rate_later/<str:video_id>/",
        VideoRateLaterDetail.as_view(),
        name="video_rate_later_detail",
    ),
    path(
        "users/<str:username>/contributor_ratings/",
        ContributorRatingList.as_view(),
        name="contributor_rating_list",
    ),
    path(
        "users/<str:username>/contributor_ratings/<str:video_id>/",
        ContributorRatingDetail.as_view(),
        name="contributor_rating_detail",
    )
]
