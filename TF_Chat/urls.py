"""TF_Chat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include
from chat import views


from django.conf.urls import url, include
from django.contrib import admin

from chat.urls import router as chat_router

from rest_framework import routers
from chat.views import QAViewSet


router = routers.DefaultRouter()
router.register(r'qa', QAViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
     url(r'^$', views.index, name='index'),
    url(r'^log/', views.log, name='log'),
    url(r'^setting/', views.setting, name='setting'),
    url(r'^top/', views.topPage, name='top'),
    url(r'^qa/', views.qa, name='qa'),
    url(r'^test/', views.test, name='test'),
    url(r'^api/', include(router.urls)),
]

