from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.core.exceptions import PermissionDenied

from accounts.models import CustomToken, User, UserDetail, Role

def user_mobile_verified(user_id):
    user_detail =  UserDetail.objects.filter(user_id=user_id).first()  
    verified = user_detail.mobile_verified
    return verified

def send_otp(phone):
    conn = conn = HttpRequest.client.HTTPSConnection("api.msg91.com")
    authkey = settings.AUTH_KEY
    template = settings.TEMPLATE_ID
    headers = {'content-type': "application/json"}
    url = 'https://api.msg91.com/api/v5/otp?authkey='+authkey + \
        '&template_id='+template+'&mobile='+phone+'&country=91'
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

def delete_active_token(token):
    get_object_or_404(CustomToken, key=token).delete()
    return True

def extract_role_permissions(role_id):
    # get role object using role_id
    role_obj = Role.objects.get(id=role_id)
    # split each permission
    perm_list = role_obj.permissions.split(",")

    return extract_permissions(perm_list)


def extract_permissions(perm_list):
    permissions = list()
    # loop through each permission
    for permission in perm_list:
        # split each permission to get app, table and permission
        perm_expand = permission.split("|")
        print(perm_expand)
        print("pppppppppp")
        # make a dictionary of the whole permission
        perm_dict = {
            "module_name": perm_expand[0],
            "table_name": perm_expand[1],
            "perm_name": perm_expand[2]
        }
        # append current permission dictionary to master list of permissions
        permissions.append(perm_dict)
    
    return permissions

def find_permission(permission_name , role):
    permissions = extract_role_permissions(role)
    for permission in permissions:
        if permission["perm_name"].lower() == permission_name.lower():
            return True
    raise PermissionDenied

def is_authorized(permission, user_id):
    user_obj = get_object_or_404(User, pk=user_id)

    is_authorized = user_obj.has_perm(permission)
    # if not authorized then raise error
    if not is_authorized:
        raise PermissionDenied

    return True