from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from django.db.models import Max
from registration.models import *
from solo.models import *
import datetime
import string
import random
from rest_framework.exceptions import APIException

#for testing twilio send sms
from twilio.rest import Client
# from twilio_api import settings
account = "ACXXXXXXXXXXXXXXXXX"
token = "YYYYYYYYYYYYYYYYYY"

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

def id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class RegistrationSerializer(serializers.ModelSerializer):
    name=serializers.CharField(allow_blank=True)
    profile_image=serializers.CharField(allow_blank=True)
    country_code=serializers.CharField(allow_blank=True)
    mobile=serializers.CharField(allow_blank=True)
    nationality=serializers.CharField(allow_blank=True)
    # lat=serializers.CharField(allow_blank=True)
    # lon=serializers.CharField(allow_blank=True)
    social_id=serializers.CharField(allow_blank=True)
    login_type = serializers.CharField(allow_blank=True)
    device_type = serializers.CharField(allow_blank=True)
    device_key = serializers.CharField(allow_blank=True)
    u_id = serializers.CharField(allow_blank=True, read_only=True)
    token = serializers.CharField(allow_blank=True,read_only=True)
    created_on = serializers.CharField(allow_blank=True, read_only=True)

    class Meta:
        model=RegisteredUser
        fields=('name','profile_image','country_code','mobile','nationality','social_id',
        'login_type','device_type','device_key','u_id','created_on','token')

    def validate(self,data):
        name=data['name']
        country_code=data['country_code']
        mobile=data['mobile']
        nationality=data['nationality']
        # lat=data['lat']
        # lon=data['lon']
        social_id=data['social_id']
        login_type=data['login_type']
        device_type=data['device_type']
        device_token=data['device_key']

        if not social_id or social_id=="":
            raise APIException({
                'success':'False',
                'message':'Please provide social id',
            })
        ruser=RegisteredUser.objects.filter(social_id=social_id).first()
        if not ruser:
            # if not name or name=="":
            #     raise APIException({
            #         'success':'False',
            #         'message':'Please provide name',
            #     })
            if not nationality or nationality=="":
                raise APIException({
                    'success':'False',
                    'message':'Please provide nationality',
                })
            # if not lat or lat=="":
            #     raise APIException({
            #         'success':'False',
            #         'message':'Please provide lat',
            #     })
            # if not lon or lon=="":
            #     raise APIException({
            #         'success':'False',
            #         'message':'Please provide lon',
            #     })
            # if not country_code or country_code=='':
            #     raise APIException({
            #         'success':'False',
            #         'message':'Please provide country code',
            #     })
            if not mobile or mobile=='':
                raise APIException({
                    'success':'False',
                    'message':'Please provide mobile',
                })
        if not login_type or login_type=="":
            raise APIException({
                'success':'False',
                'message':'Please provide login type',
            })
        if login_type not in ('1','2'):
            raise APIException({
                'success':'False',
                'message':'Please provide a valid login type',
            })
        if not device_type or device_type=="":
            raise APIException({
                'success':'False',
                'message':'Please provide device type',
            })
        if device_type not in ('1','2','3'):
            raise APIException({
                'success':'False',
                'message':'Please provide a valid device type',
            })
        if not device_token or device_token=="":
            raise APIException({
                'success':'False',
                'message':'Please provide device token',
            })
        return data

    def create(self,validated_data):
        name=validated_data['name']
        # profile_image=self.context['request'].FILES.get('profile_image')
        profile_image=self.validated_data['profile_image']
        country_code=validated_data['country_code']
        mobile=validated_data['mobile']
        nationality=validated_data['nationality']
        # lat=validated_data['lat']
        # lon=validated_data['lon']
        social_id=validated_data['social_id']
        login_type=validated_data['login_type']
        device_type=validated_data['device_type']
        device_token=validated_data['device_key']

        nationality=CountryCode.objects.filter(country=nationality).first()
        level=Level.objects.filter(level=1).first()
        ruser=RegisteredUser.objects.filter(social_id=social_id).first()
        if ruser:
            print('===hello====')
            user=ruser.user
        else:
            print("===hi===")
            user = User(
                username=social_id,
            )
            user.set_password(id_generator(10))
            user.save()
            if profile_image:
                print('inside profile image------------')
                ruser=RegisteredUser(
                    name=name,
                    profile_image=profile_image,
                    country_code=country_code,
                    mobile=mobile,
                    nationality=nationality,
                    # lat=lat,
                    # lon=lon,
                    social_id=social_id,
                    login_type=login_type,
                    device_type=device_type,
                    device_token=device_token,
                    user=user,
                    level=level,
                )
                ruser.save()
            else:
                ruser=RegisteredUser(
                    name=name,
                    country_code=country_code,
                    mobile=mobile,
                    nationality=nationality,
                    # lat=lat,
                    # lon=lon,
                    social_id=social_id,
                    login_type=login_type,
                    device_type=device_type,
                    device_token=device_token,
                    user=user,
                    level=level,
                )
                ruser.save()

        obj=UserContactList.objects.filter(contact_country_code=country_code,contact_mobile=mobile).first()
        if obj:
            obj.contact_status = '3'
            obj.save()

        validated_data['u_id']=ruser.id
        validated_data['created_on']=ruser.created_on
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        token = 'JWT '+token
        validated_data['token'] = token
        return validated_data

class CountryCodeListSerializer(serializers.ModelSerializer):
    class Meta:
        model=CountryCode
        fields=('__all__')

class AddContactListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100,allow_blank=True)
    country_code = serializers.CharField(max_length=10,allow_blank=True)
    mobile = serializers.CharField(max_length=15,allow_blank=True)

    class Meta:
        model = UserContactList
        fields= ('name','country_code','mobile')

    def create(self,validated_data):
        name=validated_data['name']
        country_code=validated_data['country_code']
        mobile=validated_data['mobile']
        ruser = self.context['ruser']
        list_obj=UserContactList.objects.filter(contact_country_code=country_code,contact_mobile=mobile).first()
        if not list_obj:
            ucl=UserContactList(
                user=ruser,
                name=name,
                contact_country_code=country_code,
                contact_mobile=mobile,
                contact_status='1',
            )
            ucl.save()
        return validated_data

class SendInvitationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100,allow_blank=True)
    country_code = serializers.CharField(max_length=10,allow_blank=True)
    mobile = serializers.CharField(max_length=15,allow_blank=True)
    class Meta:
        model = UserContactList
        fields= ('name','country_code','mobile')
    def create(self,validated_data):
        name=validated_data['name']
        country_code=validated_data['country_code']
        mobile=validated_data['mobile']
        ruser = self.context['ruser']
        url=self.context['url']
        obj=UserContactList.objects.filter(user=ruser,contact_country_code=country_code,contact_mobile=mobile).first()
        if not obj:
            obj=UserContactList(
                user=ruser,
                name=name,
                contact_country_code=country_code,
                contact_mobile=mobile,
            )

        #below 2 lines will use after getting twilio credential
        # client = Client(account,token)
        # message = client.messages.create(to=country_code+mobile, from_='YOUR TWILIO NUMBER', body=url)

        obj.contact_status='2'
        obj.save()

        return validated_data

class Screen_5_Serializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()
    max_points = serializers.SerializerMethodField()
    class Meta:
        model = RegisteredUser
        fields = ('id','name','profile_image','level','max_points','total_points','is_all_level_completed')

    def get_level(self,instance):
        return instance.level.level

    def get_max_points(self,instance):
        return instance.level.max_points

class GetAllLevelSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField()
    points=serializers.SerializerMethodField()
    levels=serializers.SerializerMethodField()
    progressbar=serializers.SerializerMethodField()
    class Meta:
        model=Level
        fields=('name','points','levels','progressbar')
    def get_name(self,instance):
        return instance.name
    def get_points(self, instance):
        points=Level.objects.filter(type=instance).aggregate(Max('max_points'))
        return points['max_points__max']
    def get_levels(self,instance):
        # print(';;;;;;;;;;;;;;;;;;;;;;;;;')
        # print(Level.objects.filter(type=instance).order_by('-level'))
        if Level.objects.filter(type=instance):
            right=Level.objects.filter(type=instance).order_by('-level').first().level
            left=Level.objects.filter(type=instance).order_by('level').first().level
            return 'LEVEL '+str(left)+' - '+str(right)
        return 'LEVEL null - null'
    def get_progressbar(self,instance):
        if Level.objects.filter(type=instance):
            l = Level.objects.filter(type=instance).order_by('-level').first()
            ins_max_level = int(l.level)
            request = self.context['request']
            user = request.user
            ruser = RegisteredUser.objects.filter(user=user).first()
            ruser_level = int(ruser.level.level)
            res = int((ruser_level*100)/ins_max_level)
            return res
        return 'null'

        # if Level.objects.filter(type=instance):
        #     max_points=Level.objects.filter(type=instance).aggregate(Max('max_points'))
        #     print(max_points)
        #     highest_max_points=Level.objects.all().order_by('-level').first().max_points
        #     res = int((max_points['max_points__max']*100)/highest_max_points)
        #     return res
        # return 'null'

class Screen_10_Serializer(serializers.ModelSerializer):
    level_name = serializers.SerializerMethodField()
    current_level = serializers.SerializerMethodField()
    next_level = serializers.SerializerMethodField()
    max_points = serializers.SerializerMethodField()
    game_played = serializers.SerializerMethodField()
    total_win = serializers.SerializerMethodField()
    total_lost = serializers.SerializerMethodField()
    total_points = serializers.SerializerMethodField()
    all_levels = serializers.SerializerMethodField()
    class Meta:
        model=RegisteredUser
        fields=('level_name','current_level','next_level','total_points','max_points',
        'game_played','total_win','total_lost','total_points','all_levels')

    def get_level_name(self,instance):
        return instance.level.type.name
    def get_current_level(self,instance):
        return instance.level.level
    def get_next_level(self,instance):
        cur=instance.level.level
        next=Level.objects.filter(level=(cur+1)).first()
        if next:
            return next.level
        else:
            return 'No next level available'
    def get_max_points(self,instance):
        return instance.level.max_points
    total_game_played=''
    total_game_win=''
    def get_game_played(self,instance):
        self.total_game_played = Round.objects.filter(player=instance).values('game').distinct().count()
        return self.total_game_played
        # return GamePlayerManager.objects.filter(player=instance).count()
    def get_total_win(self,instance):
        self.total_game_win = GamePlayerManager.objects.filter(player=instance,is_game_winner=True).count()
        return self.total_game_win
    def get_total_lost(self,instance):
        return self.total_game_played - self.total_game_win
        # return GamePlayerManager.objects.filter(player=instance,is_game_winner=False).count()
    def get_total_points(self,instance):
        return instance.total_points
    
    def get_all_levels(self,instance):
        request = self.context['request']
        queryset = LevelType.objects.all()
        serializer = GetAllLevelSerializer(queryset, many=True, context={'request':request})
        return serializer.data

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredUser
        fields = '__all__'

class OnlyProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredUser
        fields = ('profile_image',)

class UserDetailBasedOnIdSerializer(serializers.ModelSerializer):
    class Meta:
        model=RegisteredUser
        fields='__all__'

class MultipleUserDetailSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()
    max_points = serializers.SerializerMethodField()
    class Meta:
        model = RegisteredUser
        fields = ('id','name','profile_image','level','max_points','total_points','is_all_level_completed')

    def get_level(self,instance):
        if instance.level:
            return instance.level.level
        return ''

    def get_max_points(self,instance):
        if instance.level:
            return instance.level.max_points
        return ''

class GetGroupDetail(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id','name')

class GetNotificationListSerializer(serializers.ModelSerializer):
    created_on=serializers.SerializerMethodField()
    from_detail=serializers.SerializerMethodField()
    class Meta:
        model=UserNotification
        fields=('id','notification','created_on','status','req_type','from_detail')
    def get_created_on(self,instance):
        return int(datetime.datetime.timestamp(instance.created_on))
    def get_from_detail(self,instance):
        ref_id=instance.ref_id
        serializer=''
        if instance.req_type=='1' or instance.req_type=='3' or instance.req_type=='4':
            user = RegisteredUser.objects.filter(id=ref_id).first()
            serializer = MultipleUserDetailSerializer(user,context={'request':self.context['request']})
        elif instance.req_type=='2':
            gr = Group.objects.filter(id=ref_id).first()
            serializer = GetGroupDetail(gr,context={'request':self.context['request']})
        if serializer:
            return serializer.data
        return ''

class GetFriendListSerializer(serializers.ModelSerializer):
    created_on = serializers.SerializerMethodField()
    detail = serializers.SerializerMethodField()
    class Meta:
        model = UserFriendList
        fields = ('id','status','created_on','detail')
    def get_created_on(self,instance):
        return int(datetime.datetime.timestamp(instance.created_on))
    def get_detail(self,instance):
        ref = instance.friend
        # user = RegisteredUser.objects.filter(id=ref).first()
        serializer = MultipleUserDetailSerializer(ref,context={'request':self.context['request']})
        if serializer:
            return serializer.data
        return ''



class GroupJoinedMembersSerializer(serializers.ModelSerializer):
    joined_on = serializers.SerializerMethodField()
    member_detail = serializers.SerializerMethodField()
    class Meta:
        model = GroupJoinedMembers
        fields = ('joined_on','member_detail')
    def get_joined_on(self,instance):
        return int(datetime.datetime.timestamp(instance.joined_on))
    def get_member_detail(self,instance):
        serializer = MultipleUserDetailSerializer(instance.ruser,context={'request':self.context['request']})
        if serializer:
            return serializer.data
        return ''
        
class GetJoinedGroupDetailSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField()
    number_of_players=serializers.SerializerMethodField()
    joined_on = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    class Meta:
        model = GroupJoinedMembers
        fields = ('id','name','number_of_players','joined_on')
    def get_name(self,instance):
        return instance.group.id
    def get_joined_on(self,instance):
        return int(datetime.datetime.timestamp(instance.joined_on))
    def get_name(self,instance):
        return instance.group.name
    def get_number_of_players(self,instance):
        return instance.group.number_of_players
        
class GetGroupMembersSerializer(serializers.ModelSerializer):
    created_on = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
    class Meta:
        model = Group
        fields = ('id','name','number_of_players','created_on','members')
    def get_created_on(self,instance):
        return int(datetime.datetime.timestamp(instance.created_on))
    def get_members(self,instance):
        request = self.context['request']
        queryset=GroupJoinedMembers.objects.filter(group=instance)
        serializer = GroupJoinedMembersSerializer(queryset,many=True,context={'request':request})
        if serializer:
            return serializer.data
        return ''

class GetGroupDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id','name','number_of_players','created_on')
    def get_created_on(self,instance):
        return int(datetime.datetime.timestamp(instance.created_on))


class GetEditProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    class Meta:
        model=RegisteredUser
        fields=('name','profile_image')
    def get_profile_image(self,instance):
        if instance.profile_image:
            if instance.profile_image_file:
                return instance.profile_image_file.url
            else:
                return instance.profile_image
        return ''
    
class EditProfileSerializer(serializers.ModelSerializer):
    name=serializers.CharField(allow_blank=True)
    profile_image = serializers.ImageField(required=False)
    class Meta:
        model=RegisteredUser
        fields=('name','profile_image')

    def validate(self,data):
        name=data['name']
        if not name or name=="":
            raise APIException({
                'success':'False',
                'message':'Please provide name',
            })
        return data
    def create(self,validated_data):
        user=self.context['request'].user
        ruser = RegisteredUser.objects.filter(user=user).first()
        name=validated_data['name']
        profile_image=self.context['request'].FILES.get('profile_image')
        if profile_image:
            ruser.name = name
            ruser.profile_image_file = profile_image
            ruser.save()
            ruser.profile_image = ruser.profile_image_file.url
            ruser.save()
        else:
            ruser.name = name
            ruser.save()
        # validated_data['name']=ruser.name
        # if ruser.profile_image:
        #     print(ruser.profile_image)
        #     validated_data['profile_image']=ruser.profile_image_file
        # else:
        #     validated_data['profile_image']=''
        return validated_data

            






        

