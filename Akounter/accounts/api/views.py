from accounts.models import *
from accounts.api.tokens import account_activation_token
from accounts.api.serializer import *
from master.models import VersionControl
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from fcm_django.models import FCMDevice
from helpers.views import (
    user_mobile_verified,
    send_otp,
    delete_active_token
)

class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        app_login = request.query_params.get('app_login',None)
        if app_login:
            fcm = request.data["fcm_token"]
        user = authenticate(username=username, password=password)
        user_exists = User.objects.filter(username=username, is_active=True).first()
        if user is None:
            user = User.objects.filter(mobile__endswith=username).first()
            if user:
                username = user.username
                user = authenticate(username=username, password=password)
                user_exists = User.objects.filter(username=username, is_active=True).first()
            elif user_exists is not None:
                return Response({"success":"false", "error": "Password is incorrect!"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"success":"false", "error": "User not exist!"}, status=status.HTTP_400_BAD_REQUEST)
        device_id = request.data.get("device_id", False)
        if not device_id:
            return Response({"success":"false", "error":"Device id not found!"}, status=status.HTTP_400_BAD_REQUEST)
        if user is not None:
            if user.is_active:
                user_verfied = user_mobile_verified(user.id)
                user_name = str(user.first_name) + " " + str(user.last_name)
                if user_verfied == True:
                    token = CustomToken(user=user, device_id=device_id)
                    token = token.save()
                    if app_login:
                        user_id = user.id
                        fb = User.objects.get(id=user.id)
                        try:
                            devices = FCMDevice.objects.get(user=user_id)
                        except FCMDevice.DoesNotExist:
                            devices = None
                        if devices is None:
                            device = FCMDevice()
                            device.user = user
                            device.active = True
                            device.registration_id = fcm
                            device.type = "android"
                            device.name = "Mobile"
                            device.save()
                        else:
                            devices.active = True
                            devices.registration_id = fcm
                            devices.save()
                    login(request, token.user)

                    return Response({"success":"true","data":"Successfully logged in","token": token.key, "user_id":user.id,"username":user_name}, status=status.HTTP_200_OK)
                else:
                    send = send_otp(user.mobile)
                    return Response({"success":"false", "error": "User is not Verified! Please Verify Your mobile number","user_id":user.id,"device_id":device_id}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"success":"false", "error": "User is not active!"}, status=status.HTTP_400_BAD_REQUEST)
        elif user_exists is not None:
            return Response({"success":"false", "error": "Password is incorrect!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"success":"false", "error": "User not exist!"}, status=status.HTTP_400_BAD_REQUEST)


# logout view
class LogoutAPIView(APIView):

    def post(self, request):
        token = (request.headers["Authorization"])[6:]
        delete_active_token(token)
        request.session.flush()
        return Response({"success":"true", "data": "Logout successful."}, status=status.HTTP_200_OK)