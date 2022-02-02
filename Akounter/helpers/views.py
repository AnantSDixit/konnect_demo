from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.core.exceptions import PermissionDenied
import pandas as pd
import sqlalchemy

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

def database_connectivity():
    database_ip         = settings.DATABASES['default']['HOST']
    database_username   = settings.DATABASES['default']['USER']
    database_password   = settings.DATABASES['default']['PASSWORD']
    database_name       = settings.DATABASES['default']['NAME']
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                        format(database_username, database_password, 
                                                database_ip, database_name))
    return database_connection

def get_dashboard_election_filter_data(user_id,booth_id):
    conn = database_connectivity()
    # print(booth)
    # if city == '':
    if len(booth_id) == 1:
        booth_id = "("+ str(booth_id[0]) + ")"
    else:
        booth_id = tuple(booth_id)
    user_data = pd.read_sql_query('select  case when t11.id is not null then 1 else 0 end  as connection_flag  \
                    ,count(t10.voted) as voted_or_nonvoted_count, t10.voted,city_name as company_city_name ,master_city.id as company_city_id,name as booth_name,master_boothmaster.id as booth_id,t13.tag_value as firstcontact,t13.reference_id as firstcontact_id, t14.tag_value as coremember,t14.reference_id as coremember_id,t15.tag_value as preferences,t15.reference_id as preferences_id \
                from (select id,mrn_no,first_name,last_name,mobile,email,company_city_id,alt_mobile_1,alt_mobile_2,voted,active,booth_no_id from master_centralizeddata where booth_no_id in '+str(booth_id)+') as t10 \
                    left join (select id , mrn_no, first_name,last_name,mobile,email,company_city_id,alt_mobile_1,alt_mobile_2,connection_centralized_id from konnect_connection where parent_user_id = '+str(user_id)+' and connection_centralized_id is not null and status = 1) as t11 on t10.id = t11.connection_centralized_id inner join master_boothmaster on master_boothmaster.id = t10.booth_no_id \
                    left join (select tag_value,meeting_connection_id_id,reference_id from tags_tag where rel_type = "mention" and rel_id = 4) as t13 on t13.meeting_connection_id_id = t11.id\
                    left join (select tag_value,meeting_connection_id_id,reference_id from tags_tag where rel_type = "mention" and rel_id = 3) as t14 on t14.meeting_connection_id_id = t11.id\
                    left join (select tag_value,meeting_connection_id_id,reference_id from tags_tag where rel_type = "preferences") as t15 on t15.meeting_connection_id_id = t11.id\
                    inner join master_city  on  master_city.id = master_boothmaster.city_id \
                    group by connection_flag , t10.voted  ,company_city_name,company_city_id, booth_name, booth_id,firstcontact,coremember,firstcontact_id,coremember_id,preferences,preferences_id\
                ' ,con = conn)

     
    # user_data.drop(["tag_value","meeting_connection_id_id"],axis="columns",inplace = True)
    user_data = user_data.fillna('')
    user_data = user_data.to_dict("record")
    # total_count = {"total_count":total_data}
    # user_data.append(total_data)

    return user_data