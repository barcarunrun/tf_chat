"""
from rest_framework import routers
from .views import QAViewSet
from django.conf.urls import url


router = routers.DefaultRouter()
router.register(r'qa', QAViewSet)
"""