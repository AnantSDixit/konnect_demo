
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.db.models import CharField,Value as V
from django.conf import settings
from django.db.models import Q
from django.db.models import F
from numpy import append
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
import pandas as pd
import requests

from accounts.models import UserDetail,User,UserRoleMap
from konnect.models import *
from helpers.views import (
    find_permission,
    is_authorized

)
from tags.models import (
    Tag
)
from konnect.api.serializer import *


class Connectiontaglist(ViewSet):
    def list(self, request):
        try:
            campaign_flag = request.headers["campaign_flag"]
        except:
            campaign_flag = request.query_params.get('campaign_flag',None)
        if campaign_flag == 1 or campaign_flag == "1":
            campaign = get_object_or_404(UserRoleMap, user=request.user,active =True).role.campaign.campaign_user
            role = get_object_or_404(UserRoleMap, user=request.user,active =True).role.id
            find_permission("view_own_connection",role)
            user_id = campaign.id
        else:
            is_authorized("konnect.view_own_connection", request.user.id)
            user_id = request.user.id
        queryset = pd.DataFrame(list(Tag.objects.annotate(
                    ids = F('reference_id')).filter(Q(rel_id=3) | Q(rel_id=4) | Q(rel_id=2),meeting_connection_id_id__parent_user_id=user_id,active = True,meeting_connection_id_id__status = 1,rel_type = "mention").values("ids","tag_value").distinct()))
        queryset = queryset.drop_duplicates(subset=['ids'])
        data = queryset.to_dict("record")
        return Response({"success":"true", "data":data}, status=status.HTTP_200_OK)

class SearchTagConnection(APIView):

    def get(self, request):
        abc = {}
        try:
            campaign_flag = request.headers["campaign_flag"]
        except:
            campaign_flag = request.query_params.get('campaign_flag',None)
        if campaign_flag == 1 or campaign_flag == "1":
            campaign = get_object_or_404(UserRoleMap, user=request.user,active =True).role.campaign.campaign_user
            role = get_object_or_404(UserRoleMap, user=request.user,active =True).role.id
            find_permission("view_own_connection",role)
            user_id = campaign.id
        else:
            is_authorized("konnect.view_own_connection", request.user.id)
            user_id = request.user.id
        search = request.data["search"]
        #queryset = Tag.objects.filter(tag_value = search).values_list('meeting_connection_id', flat=True)
        queryset = Tag.objects.filter(tag_value = search,reference_id__isnull = False, meeting_connection_id__parent_user_id = user_id).values(
            'meeting_connection_id__id','meeting_connection_id__mrn_no','meeting_connection_id__first_name',
            'meeting_connection_id__last_name','meeting_connection_id__mobile','meeting_connection_id__email',
            'meeting_connection_id__region','meeting_connection_id__city')
        #for id in queryset:
            #id['meeting_connection_id']
        #print(id)
        #abc = abc.update(queryset)
        #ids_value = xyz.values()
        #ids = list(ids_value)
        #for i in queryset:
            #queryset1 = Connection.objects.filter(id = i).values()
            #print(queryset1)
            #abc = abc.update(queryset)
            
        #print(abc)
        #print(queryset1)
        return Response({"success":"true","data":queryset})
