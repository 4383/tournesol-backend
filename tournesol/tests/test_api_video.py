from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from ..models import Video


class VideoApi(TestCase):
    """
    TestCase of the video API.
    """

    _video_id_01 = "video_id_01"
    _video_id_02 = "video_id_02"
    _video_id_03 = "video_id_03"
    _video_id_04 = "video_id_04"
    _list_of_videos = []

    def setUp(self):
        self._list_of_videos = Video.objects.bulk_create([
            Video(video_id=self._video_id_01, name=self._video_id_01),
            Video(video_id=self._video_id_02, name=self._video_id_02),
            Video(video_id=self._video_id_03, name=self._video_id_03),
            Video(video_id=self._video_id_04, name=self._video_id_04)
        ])

    def test_anonymous_can_list(self):
        """
        An anonymous user can list all videos.

        The current implementation is a minimal one that doesn't check the
        order of the videos in the response yet, but it performs several tests
        ensuring the API returns the expected videos given the parameters
        provided.
        """
        client = APIClient()

        # test a request without query parameters
        response = client.get(
            reverse("tournesol:video-list"), format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        returned_video_ids = [video["video_id"] for video in response.data["results"]]
        existing_video_ids = [video.video_id for video in self._list_of_videos]

        self.assertEqual(set(returned_video_ids), set(existing_video_ids))
        self.assertEqual(response.data["count"], len(self._list_of_videos))
        self.assertEqual(len(response.data["results"]), len(self._list_of_videos))

        # test a request with the limit query parameter
        limit = 2
        response = client.get(
            reverse("tournesol:video-list"), {"limit": limit}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], len(self._list_of_videos))
        self.assertEqual(len(response.data["results"]), limit)

        # test that a huge limit doesn't break anything
        limit = 10000
        response = client.get(
            reverse("tournesol:video-list"), {"limit": limit}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        returned_video_ids = [video["video_id"] for video in response.data["results"]]

        self.assertEqual(set(returned_video_ids), set(existing_video_ids))
        self.assertEqual(response.data["count"], len(self._list_of_videos))
        self.assertEqual(len(response.data["results"]), len(self._list_of_videos))

    def test_upload_video_without_API_key(self):
        factory = APIClient()
        response = factory.post(
            "/video/",
            {'video_id':'NeADlWSDFAQ'},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_upload_video_already_exist_without_API_key(self):
        Video.objects.create(video_id="NeADlWSDFAQ")
        client = APIClient()
        data={'video_id':'NeADlWSDFAQ'}
        response = client.post(
            "/video/",
            data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_video_incorrect_id(self):
        factory = APIClient()
        response = factory.post(
            "/video/",
            {'video_id':'AZERTYUIOPV3'}, # length of 12
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = factory.post(
            "/video/",
            {'video_id':'AZERTYUPV3'}, # length of 10
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def get_existing_video(self):
        Video.objects.create(video_id='NeADlWSDFAQ')
        factory = APIClient()
        response = factory.get(
            "/video/",
            {'video_id':'NeADlWSDFAQ'},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response[0].video_id, 'NeADlWSDFAQ')
    
    def get_existing_video(self):
        factory = APIClient()
        response = factory.get(
            "/video/",
            {'video_id':'NeADlWSDFAQ'},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)