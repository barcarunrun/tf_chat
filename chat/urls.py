from rest_framework import routers
from .views import QAViewSet


router = routers.DefaultRouter()
router.register(r'qa', QAViewSet)