from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny,IsAuthenticated,)
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from registration.models import *
from .serializers import *
#

import logging
logger = logging.getLogger('accounts')

class RegistrationView(APIView):
    def post(self,request,*args,**kwargs):
        logger.debug('Registration view post called')
        logger.debug(request.data)
        serializer=RegistrationSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success':'True',
                'message':'Registration Successfull',
                'data':serializer.data,
            },status=200)
        else:
            return Response({
                'success':'False',
                'message':'Registration Failed',
            },status=400)

class CountryCodeListView(APIView):
    def get(self,request,*args,**kwargs):
        logger.debug('Country code list get called')
        logger.debug(request.data)
        queryset=CountryCode.objects.all()
        serializer=CountryCodeListSerializer(queryset,many=True)
        return Response({
            'message':'Data retrieved successfully',
            'success':'True',
            'data':serializer.data,
        },status=200,)
        #
        # for i in queryset:
        #     data.append(i.nationality)

class AddContactListView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def post(self,request,*args,**kwargs):
        logger.debug('Add contact view post called')
        logger.debug(request.data)
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        print(request.data)
        serializer = AddContactListSerializer(data=request.data, context={'ruser':ruser,'request':request}, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Data updated successfully',
                'success':'True',
            },status=200)
        return Response({
            'message':'Data updated failed',
            'success':'False',
        },status=400)

class AddAppLinkView(APIView):
    def post(self,request,*args,**kwargs):
        logger.debug('Add app link post called')
        logger.debug(request.data)
        url=request.data['link']
        obj=AppLink.objects.all().first()
        if obj:
            obj.url=url
        obj = AppLink(
            url=url,
        )
        obj.save()
        return Response({
            'message':'Link saved Successfully',
            'success':'True',
        },status=200)

class SendInvitationView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def post(self,request,*args,**kwargs):
        logger.debug('Send invite view post called')
        logger.debug(request.data)
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        url_obj=AppLink.objects.all().first()
        url=url_obj.url
        serializer = SendInvitationSerializer(data=request.data,context={'request':request,'ruser':ruser,'url':url},many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Invitations sent to the selected contacts.',
                'success':'True',
            },status=200)
        return Response({
            'message':'Can not send invitation.',
            'success':'False',
            'errors':serializer.errors
        },status=400,)

class SearchCountry(ListAPIView):
    def get_queryset(self,request,*args,**kwargs):
        query=self.request.GET.get('q',None)
        query_list=CountryCode.objects.all()
        if query:
            query_list=query_list.filter(Q(country__icontains=query.lower())).distinct()
        return query_list
    def list(self,request,*args,**kwargs):
        logger.debug('Search country called')
        logger.debug(request.data)
        qs=self.get_queryset(request)
        data=CountryCodeListSerializer(qs,many=True,context={'request':self.request}).data
        return Response({
            'message':'Data retrieved successfully',
            'success':'True',
            'data':data,
        },status=200,)

class Screen_5_View(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def get(self,request,*args,**kwargs):
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        serializer=Screen_5_Serializer(ruser,context={'request':request})
        return Response({
            'message':'Data retrieved successfully',
            'success':'True',
            'data':serializer.data,
        },status=200)

class Screen_10_View(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def get(self,request,*args,**kwargs):
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        serializer=Screen_10_Serializer(ruser,context={'request':request})
        return Response({
            'message':'Data retrieved successfully',
            'success':'True',
            'data':serializer.data,
        },status=200,)

class UserDetailView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def get(self,request,*args,**kwargs):
        user = request.user
        ruser = RegisteredUser.objects.filter(user=user).first()
        serializer = UserDetailSerializer(ruser,context={'request':request})
        if serializer:
            
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },status=200,)
        return Response({
            'message':'Failed to retrieve data',
            'success':'False',            
        },status=400,)

class OnlyProfileImageView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def get(self,request,*args,**kwargs):
        user = request.user
        ruser = RegisteredUser.objects.filter(user=user).first()
        serializer = OnlyProfileImageSerializer(ruser,context={'request':request})
        if serializer:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },status=200,)
        return Response({
            'message':'Failed to retrieve data',
            'success':'False',            
        },status=400,)
        
class UserDetailBasedOnIdView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def post(self,request,*args,**kwargs):
        id=request.data['id']
        print(id)
        if id:
            queryset=RegisteredUser.objects.filter(id=id).first()
            serializer=UserDetailBasedOnIdSerializer(queryset,context={'request':request})
            if serializer:
                return Response({
                    'message':'Data retrieved successfully',
                    'success':'True',
                    'data':serializer.data,
                },status=200)
            return Response({
                'message':'Failed to retrieve data',
                'success':'False',
            },status=400)
        return Response({
            'message':'Please provide user id',
            'success':'False',
        },status=400)

class MultipleUserDetailView(APIView):
    # permission_classes=(IsAuthenticated,)
    # authentication_classes=(JSONWebTokenAuthentication,)
    def post(self,request,*args,**kwargs):
        ids=request.data['ids']
        if not ids or ids=="":
            return Response({
                'message':'Please provide ids',
                'success':'False',
            },status=400)
        if ',' in ids:
            id_list=ids.split(',')
        else:
            id_list=[ids]
        queryset=RegisteredUser.objects.filter(id__in=id_list)
        serializer=MultipleUserDetailSerializer(queryset,many=True,context={'request':request})
        if serializer.data:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },status=200)
        return Response({
            'message':'Data retrieve failed',
            'success':'False',
        },status=400)


from pyfcm import FCMNotification
class SendRequestView(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        notification=request.data['notification_text']
        if not notification or notification == '':
            return Response({
                'message':'Please provide notification text',
                'success':'False',
            },status=400)
        fid=request.data['friend_id']
        if not fid or fid == '':
            return Response({
                'message':'Please provide friend id',
                'success':'False',
            },status=400)
        friend=RegisteredUser.objects.filter(id=fid).first()
        if not friend:
            return Response({
                'message':'Invalid friend id',
                'success':'False',
            },status=400)
        req_type=request.data['request_type']
        if not req_type or req_type == '':
            return Response({
                'message':'Please provide request type',
                'success':'False',
            },status=400)
        if req_type not in ('1','2','3','4'):
            return Response({
                'message':'Request type value is incorrect',
                'success':'False',
            },status=400)
        
        if req_type in ('1','3','4'):
            user=request.user
            ruser=RegisteredUser.objects.filter(user=user).first()
            ref_id=ruser.id
        else:
            group_id=request.data['group_id']
            if not group_id or group_id=="":
                return Response({
                    'message':'Please provide group id',
                    'success':'False',
                },status=400)
            ref=Group.objects.filter(id=group_id).first()
            if not ref:
                return Response({
                    'message':'Please provide valid group id',
                    'success':'False',
                },status=400)
            ref_id=ref.id

        
        un=UserNotification(
            notification=notification,
            user=friend,
            req_type=req_type,
            ref_id=ref_id
        )
        un.save()
        

        if req_type == '1':
            gr=GameRequestList(
                grto=friend,
                grfrom=ruser
            )
            gr.save()
        if req_type == '4':
            ufl=UserFriendList(
                player=friend,
                friend=ruser
            )
            ufl.save()

        api_key=''
        if api_key!='':
            print('inside push notification')
            push_service= FCMNotification(api_key=api_key)
            registration_id=friend.device_token
            message_title="MyGame Notification"
            message_body=notification
            result=push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
            if result:
                return Response({
                    'message':'Notification sent successfully',
                    'success':'True',
                },status=200)
            else:
                return Response({
                    'message':'Notification saved but unable to send notification',
                    'success':'True'
                },status=200)
        else:
            return Response({
                'message':'Notification saved but to send notification please provide firebase api key',
                'success':'True',
            },status=200)
class GetNotificationListView(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        user=request.user
        user=RegisteredUser.objects.filter(user=user).first()
        queryset=UserNotification.objects.filter(user=user)
        serializer=GetNotificationListSerializer(queryset,many=True,context={'request':request})
        if serializer:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },status=200)
        return Response({
            'message':'Data retrieve failed',
            'success':'False',
        },status=400)
class AcceptRequestView(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        notification_id=request.data['notification_id']
        if not notification_id or notification_id=="":
            return Response({
                'message':'Please provide notification id',
                'success':'False',
            },status=400)
        user=request.user
        un = UserNotification.objects.filter(id=notification_id).first()
        if not un:
            return Response({
                'message':'Please provide valid notification id',
                'success':'False',
            },status=400)
        if un.req_type == '1':
            user=RegisteredUser.objects.filter(user=user).first()
            ruser=RegisteredUser.objects.filter(id=un.ref_id).first()
            gr = GameRequestList.objects.filter(grto=user,grfrom=ruser).first()
            gr.status = '2'
            gr.save()
        if un.req_type == '2':
            user=RegisteredUser.objects.filter(user=user).first()
            g = Group.objects.filter(id=un.ref_id).first()
            g.number_of_players=g.number_of_players+1
            g.save()
            gjm=GroupJoinedMembers(
                group=g,
                ruser=user,
            )
            gjm.save()
        if un.req_type == '4':
            user=RegisteredUser.objects.filter(user=user).first()
            ruser=RegisteredUser.objects.filter(id=un.ref_id).first()
            ufl = UserFriendList.objects.filter(player=user,friend=ruser).first()
            ufl.status = '2'
            ufl.save()
        un.status='2'
        un.save()
        return Response({
                'message':'Request accepted successfully',
                'success':'True',
            },status=200)
class DeclineRequestView(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        notification_id=request.data['notification_id']
        if not notification_id or notification_id=="":
            return Response({
                'message':'Please provide notification id',
                'success':'False',
            },status=400)
        user=request.user
        un = UserNotification.objects.filter(id=notification_id).first()
        if not un:
            return Response({
                'message':'Please provide valid notification id',
                'success':'False',
            },status=400)
        if un.req_type == '1':
            user=RegisteredUser.objects.filter(user=user).first()
            ruser=RegisteredUser.objects.filter(id=un.ref_id).first()
            gr = GameRequestList.objects.filter(grto=user,grfrom=ruser).first()
            gr.status = '3'
            gr.save()
        if un.req_type == '2':
            user=RegisteredUser.objects.filter(user=user).first()
            g = Group.objects.filter(id=un.ref_id).first()
            g.number_of_players=g.number_of_players+1
            g.save()
            gjm=GroupJoinedMembers(
                group=g,
                ruser=user,
            )
            gjm.save()
        if un.req_type == '4':
            user=RegisteredUser.objects.filter(user=user).first()
            ruser=RegisteredUser.objects.filter(id=un.ref_id).first()
            ufl = UserFriendList.objects.filter(player=user,friend=ruser).first()
            ufl.status = '3'
            ufl.save()
        un.status='2'
        un.save()
        return Response({
                'message':'Request declined successfully',
                'success':'True',
            },status=200)
class SendGeneralNotificatonView(APIView):
    pass
def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
class GetShareCodeView(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        user = request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        if ruser.share_code:
            return Response({
                'message':'Share code retrieved successfully',
                'success':'True',
                'data':{
                    'share_code':ruser.share_code
                }
            },status=200)
        else:
            id = id_generator()
            ruser.share_code = id
            ruser.save()
            return Response({
                'message':'Share code retrieved successfully',
                'success':'True',
                'data':{
                    'share_code':ruser.share_code
                }
            },status=200)
class GetFriendListView(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        user = request.user
        ruser = RegisteredUser.objects.filter(user=user).first()
        queryset = UserFriendList.objects.filter(player=ruser,status='2')
        serializer = GetFriendListSerializer(queryset,many=True,context={'request':request})
        if serializer:
            return Response({
                'message':'Friend List retrieved successfully',
                'success':'True',
                'data':serializer.data
            },status=200)
        return Response({
            'message':'Data retrieve failed',
            'success':'False',
        },status=400)

class CreateGroupView(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        group_name=request.data['group_name']
        number_of_players=request.data['number_of_players']
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        if not group_name or group_name=="":
            return Response({
                'message':'Please provide group name',
                'success':'False',
            },status=400)
        if not number_of_players or number_of_players=="":
            return Response({
                'message':'Please provide number of players',
                'success':'False',
            },status=400)
        
        gr=Group(
            name=group_name,
            number_of_players=number_of_players,
            created_by=ruser
        )
        gr.save()
        gjm=GroupJoinedMembers(
            group=gr,
            ruser=ruser
        )
        gjm.save()
        return Response({
            'message':'Group created successfully',
            'success':'True',
            'data':{
                'group_id':gr.id
            }
        },status=200) 
class GetGroupMembersListView(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        id=self.kwargs['pk']
        gr = Group.objects.filter(id=id).first()
        serializer = GetGroupMembersSerializer(gr,context={'request':request})
        if serializer:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },status=200)
class GetAllGroupListView(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        queryset = Group.objects.all()
        serializer = GetGroupDetailSerializer(queryset,many=True,context={'request':request})
        if serializer:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },status=200)

class GetCreatedGroupListView(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        queryset=Group.objects.filter(created_by=ruser)
        serializer = GetGroupDetailSerializer(queryset,many=True,context={'request':request})
        if serializer:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },status=200)

class GetJoinedGroupListView(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        user=request.user
        ruser=RegisteredUser.objects.filter(user=user).first()
        queryset=GroupJoinedMembers.objects.filter(ruser=ruser)
        serializer = GetJoinedGroupDetailSerializer(queryset,many=True,context={'request':request})
        if serializer:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },status=200)

class GetUserBySearchView(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        search_text=request.data['search_text']
        user=request.user
        queryset = RegisteredUser.objects.filter(is_deleted=False).exclude(user=user).exclude(user__is_superuser=True)
        if search_text:
            queryset = RegisteredUser.objects.filter(Q(is_deleted=False)&(Q(name__icontains=search_text)|Q(user__email__icontains=search_text))).exclude(user=user).exclude(user__is_superuser=True)
        serializer = MultipleUserDetailSerializer(queryset,many=True,context={'request':request})
        if serializer:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },status=200)


class RemovePlayerByAdminView(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        user=request.user
        gadmin = RegisteredUser.objects.filter(user=user).first()

        player_id=request.data['player_id']
        group_id=request.data['group_id']
        if not player_id or player_id=='':
            return Response({
                'message':'Please provide player id',
                'success':'False',
            },status=400)
        if not group_id or group_id=='':
            return Response({
                'message':'Please provide group id',
                'success':'False',
            },status=400)
        player = RegisteredUser.objects.filter(id=player_id).first()
        if not player:
            return Response({
                'message':'Please provide valid player id',
                'success':'False',
            },status=400)
        group = Group.objects.filter(id=group_id).first()
        if not group:
            return Response({
                'message':'Please provide valid group id',
                'success':'False',
            },status=400)
        if group.created_by.id != gadmin.id:
            return Response({
                'message':'You are not an admin of this group',
                'success':'False',
            },status=400)
        print(gadmin.id)
        print(player_id)
        if gadmin.id == int(player_id):
            return Response({
                'message':'You can not give your own id as player id',
                'success':'False',
            },status=400)
        GroupJoinedMembers.objects.filter(group=group,ruser=player).delete()
        return Response({
            'message':'Player deleted successfully',
            'success':'True',
        },status=200)
class RemovePlayerByOwn(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):
        group_id=request.data['group_id']
        if not group_id or group_id=='':
            return Response({
                'message':'Please provide group id',
                'success':'False',
            },status=400)
        player = RegisteredUser.objects.filter(user=request.user).first()
        group = Group.objects.filter(id=group_id).first()
        if not group:
            return Response({
                'message':'Please provide valid group id',
                'success':'False',
            },status=400)
        GroupJoinedMembers.objects.filter(group=group,ruser=player).delete()
        return Response({
            'message':'Player removed successfully',
            'success':'True',
        },status=200)
class AdminExitView(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def post(self,request,*args,**kwargs):       
        group_id=request.data['group_id']
        if not group_id or group_id=='':
            return Response({
                'message':'Please provide group id',
                'success':'False',
            },status=400)
        player = RegisteredUser.objects.filter(user=request.user).first()
        group = Group.objects.filter(id=group_id).first()
        if not group:
            return Response({
                'message':'Please provide valid group id',
                'success':'False',
            },status=400)
        GroupJoinedMembers.objects.filter(group=group,ruser=player).delete()
        gmembers_count = GroupJoinedMembers.objects.filter(group=group).count()
        if gmembers_count==0:
            group.delete()
        else:    
            tempg = GroupJoinedMembers.objects.filter(group=group).first()
            group.created_by = tempg.ruser
            group.save()
        return Response({
            'message':'Group updated successfully',
            'success':'True',
        },status=200)

class EditProfileView(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[JSONWebTokenAuthentication,]
    def get(self,request,*args,**kwargs):
        user = request.user
        ruser = RegisteredUser.objects.filter(user=user).first()
        serializer = GetEditProfileSerializer(ruser,context={'request':request})
        if serializer:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },status=200,)
        return Response({
            'message':'Failed to retrieve data',
            'success':'False',            
        },status=400,)
    def post(self,request,*args,**kwargs):
        serializer = EditProfileSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success':'True',
                'message':'Profile updated Successfully',
                # 'data':serializer.data,
            },status=200)
        else:
            return Response({
                'success':'False',
                'message':'Update Failed',
                'data':serializer.errors
            },status=400)
