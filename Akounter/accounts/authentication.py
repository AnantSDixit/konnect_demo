from rest_framework.authentication import TokenAuthentication
from accounts.models import CustomToken

class CustomTokenAuthentication(TokenAuthentication):
    model = CustomToken