from django.urls import path, include
from rest_framework.routers import DefaultRouter
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from accounts.api.views import *

router = DefaultRouter()
router.register(r'devices', FCMDeviceAuthorizedViewSet)

urlpatterns = router.urls

urlpatterns.append(path('logout/', LogoutAPIView.as_view()))
urlpatterns.append(path('login/', LoginAPIView.as_view()))
