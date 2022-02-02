from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Election.api.views import *

router = DefaultRouter()

urlpatterns = router.urls
urlpatterns.append(path('get_election_dasboard_count/', ElectionDasboardCount.as_view(), name="get_election_dasboard_count"))
urlpatterns.append(path('get_election_dasboard_filter_data/', ElectionDashboardFilterData.as_view(), name="get_election_dasboard_filter_data"))
urlpatterns.append(path('election_master/', ElectionMasterList.as_view(), name="election_master"))
urlpatterns.append(path('booth_master/', BoothMasterList.as_view(), name="booth_list"))
