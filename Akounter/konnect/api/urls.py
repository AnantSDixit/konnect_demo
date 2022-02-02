from django.urls import path
from rest_framework.routers import DefaultRouter
from konnect.api.views import *
router = DefaultRouter()
router.register(r'connection-tag-list', Connectiontaglist, basename='connection-tag-list')

urlpatterns = router.urls
urlpatterns.append(path('SearchTagConnection/', SearchTagConnection.as_view()))