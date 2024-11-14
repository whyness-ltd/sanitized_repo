#----------------------------------------------------------------------
# Whyness rest core test
#
# Copyright (c) 2021-2022, Whyness Ltd https://REMOVED
#
#----------------------------------------------------------------------
import json
import os
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from whyness_django.models import Audio

class StandardRestCoreTestCase(APITestCase):
    """
    Standard REST core tests
    """
    #fixtures = ['core.json']

    def setUp(self):
        """Set up test environment"""
        BASE_DIR = os.path.dirname(os.path.realpath(__file__))
        BASE_DIR = os.path.dirname(os.path.realpath(BASE_DIR))
        self.media_file = os.path.join(BASE_DIR, "static/silence.mp2")

    def test_audio_addnew(self):
        """Test add new audio"""

        with open(self.media_file, mode='rb') as media_file:
            data = SimpleUploadedFile(
                "silence.wav",
                media_file.read(),
                content_type="audio/x-wav"
            )
        url = reverse('api-media')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['title'], data['name'])
        self.assertEqual(response.data['status'], 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_audio_listing(self):
        """Test audio listing"""
        url = reverse('api-media')
        response = self.client.get(url, format='json')
        results=response.data[0]
        self.assertEqual(results['id'], 1)
        self.assertEqual(results['title'], "Test")

    def test_audio_detail_view(self):
        """Test audio item view"""
        url = reverse('api-media', args=[1])
        response = self.client.get(url, format='json')
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['title'], "Test")
        self.assertEqual(response.data['status'], 1)

