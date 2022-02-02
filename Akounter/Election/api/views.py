from helpers.views import get_dashboard_election_filter_data
from accounts.models import *
from master.models import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

class ElectionDasboardCount(APIView):
    
    def get(self, request):
        
        user_id = request.user.id
        campaign = Campaign.objects.filter(campaign_user_id=user_id, active=True).first()
        if campaign:
            user_detail = UserDetail.objects.filter(user_id=user_id, active=True).first() 
            region = user_detail.region
        else:
            campaign = UserRoleMap.objects.filter(user_id=user_id, active=True).values('role__campaign').first()
            if campaign:
                campaign_id = Campaign.objects.filter(id=campaign['role__campaign'], active=True).first()
                user_detail = UserDetail.objects.filter(user_id=campaign_id.campaign_user, active=True).first()
                region = user_detail.region
                user_id = campaign_id.campaign_user
            else:
                return Response({"success":"false","error":"Not connected with any campaign!"},status = status.HTTP_400_BAD_REQUEST)

        if region:
            election = ElectionMaster.objects.filter(region=region, active=True).first()
            #print(election)
            if election :
                booth = BoothMaster.objects.filter(election_id=election.id, active=True)
                #print(booth)

                if booth:
                    total_member_count = CentralizedData.objects.filter(booth_no__in=booth, active=True).count()    
                    voted_member_count = CentralizedData.objects.filter(booth_no__in=booth, voted=True, active=True).count()    
                    non_voted_member_count = int(total_member_count) - int(voted_member_count)

                    total_conn_count = Connection.objects.filter(parent_user_id=user_id,connection_centralized__booth_no__in=booth,  active=True).count()    
                    voted_conn_count = Connection.objects.filter(parent_user_id=user_id,connection_centralized__booth_no__in=booth,  connection_centralized__voted=True, active=True).count()    
                    non_voted_conn_count = int(total_conn_count) - int(voted_conn_count)

                    return Response({"success":"true","data":{"total_member":total_member_count, "total_member_voted":voted_member_count, "total_member_non_voted":non_voted_member_count, "total_connection":total_conn_count, "total_connection_voted":voted_conn_count,"total_connection_non_voted":non_voted_conn_count}},status = status.HTTP_200_OK)
                else:
                    return Response({"success":"false","error":"Booth is not available"},status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"success":"false","error":"No active Elections."},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"success":"false","error":"No Region Found"},status = status.HTTP_400_BAD_REQUEST)


class ElectionDashboardFilterData(APIView):
        
        def get(self,request):
            user_id = request.user.id
            # get campaign of logged in user from front end
            campaign = Campaign.objects.filter(campaign_user_id=user_id, active=True).first()
            if campaign:
                user_detail = UserDetail.objects.filter(user_id=user_id, active=True).first() 
                region = user_detail.region
                campaign_user_id = user_id 
            else:
                campaign = UserRoleMap.objects.filter(user_id=user_id, active=True).values('role__campaign').first()
                if campaign:
                    campaign_id = Campaign.objects.filter(id=campaign['role__campaign'], active=True).first()
                    user_detail = UserDetail.objects.filter(user_id=campaign_id.campaign_user, active=True).first()
                    region = user_detail.region
                    campaign_user_id = campaign_id.campaign_user_id 
                else:
                    return Response({"success":"false","error":"Not connected with any campaign!"},status = status.HTTP_400_BAD_REQUEST)

            if region:
                election = ElectionMaster.objects.filter(region=region, active=True).first()
                if election :
                    booth = BoothMaster.objects.filter(election_id=election.id, active=True).values_list('id', flat=True)
                    print(booth)
                    if booth:
                        booth_id = []
                        for id in booth:
                            booth_id.append(id)
                        data = get_dashboard_election_filter_data(campaign_user_id,booth_id)
                        return Response({"success":"true","data":data},status = status.HTTP_200_OK)
                    else:
                        return Response({"success":"false","error":"Booth is not available"},status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"success":"false","error":"No active Elections."},status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"success":"false","error":"Region not found"},status = status.HTTP_400_BAD_REQUEST)


class ElectionMasterList(APIView):

    def get(self, request):
       
        user_detail = UserDetail.objects.filter(user_id=request.user.id, active=True).first() 
        region = user_detail.region

        election = ElectionMaster.objects.filter(region=region, active=True).values().first()
        if election :
            return Response({"success":"true","data":election},status = status.HTTP_200_OK)
        else :
            return Response({"success":"true","data":election},status = status.HTTP_200_OK)


class BoothMasterList(APIView):

    def get(self, request):

        election_id = request.query_params.get('election_id',None)
        if election_id == None or election_id == "" :
            return Response({"success":"false","error":"Election Id is not found."},status = status.HTTP_400_BAD_REQUEST)
        else:
            booth = BoothMaster.objects.filter(election_id=election_id, active=True).values()
            if booth :
                return Response({"success":"true","data":booth},status = status.HTTP_200_OK)
            else :
                return Response({"success":"false","error":"No booth found"},status = status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        booth_id = request.data["booth_id"]
        if booth_id: 
            booth = BoothMaster.objects.filter(id=booth_id, active=True).values().first()
            if booth :
                return Response({"success":"true","data":booth},status = status.HTTP_200_OK)
            else :
                return Response({"success":"true","data":"No booth found"},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"success":"false","error":"Booth Id not found."},status = status.HTTP_400_BAD_REQUEST)