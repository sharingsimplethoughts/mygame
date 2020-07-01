from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
gender_choices=(('1','Male'),('2','Female'))
login_type_choices=(('1','Facebook'),('2','Google'))
device_type_choices=(('1','Android'),('2','Ios'),('3','Web'))
contact_status = (('1','Saved'),('2','Invited'),('3','Installed'))


class CountryCode(models.Model):
    country=models.CharField(max_length=50,blank=True,null=True)
    code=models.CharField(max_length=10,blank=True,null=True)
    def __str__(self):
        return self.country

class LevelType(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True, )

    def __str__(self):
        return self.name

class Level(models.Model):
    type = models.ForeignKey(LevelType, on_delete=models.CASCADE, related_name='l_name', default='', blank=True)
    level=models.PositiveIntegerField(default=0)
    max_points=models.PositiveIntegerField(default=0)
    def __str__(self):
        return str(self.level)+'--'+str(self.max_points)

class RegisteredUser(models.Model):
    name=models.CharField(max_length=70)
    about=models.CharField(max_length=200,blank=True,null=True)
    profile_image_file=models.ImageField(upload_to='user/profile_image',blank=True,null=True)
    profile_image=models.URLField(default='',blank=True,null=True)
    gender=models.CharField(max_length=15, choices=gender_choices,blank=True,null=True)

    country_code=models.CharField(max_length=5,blank=True,null=True)
    mobile=models.CharField(max_length=200)
    is_mobile_verified=models.BooleanField(default=False)

    lat=models.CharField(max_length=50,blank=True,null=True)
    lon=models.CharField(max_length=50,blank=True,null=True)
    zipcode=models.CharField(max_length=50,blank=True,null=True)
    street=models.CharField(max_length=200,blank=True,null=True)
    area=models.CharField(max_length=100,blank=True,null=True)
    city=models.CharField(max_length=50,blank=True,null=True)
    country=models.CharField(max_length=50,blank=True,null=True)

    social_id=models.CharField(max_length=200,blank=True,null=True)
    login_type=models.CharField(max_length=10,choices=login_type_choices)
    device_type=models.CharField(max_length=10,choices=device_type_choices)
    device_token=models.CharField(max_length=200,blank=True,null=True)

    created_on=models.DateTimeField(auto_now_add=True)
    is_deleted=models.BooleanField(default=False)
    is_approved=models.BooleanField(default=False)

    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='ruser')
    nationality=models.ForeignKey(CountryCode, on_delete=models.CASCADE, related_name='rnationality')

    level=models.ForeignKey(Level,on_delete=models.CASCADE,related_name='pl_level',blank=True,null=True)
    is_all_level_completed=models.BooleanField(default=False)
    # level=models.CharField(max_length=2, default='')
    total_points=models.PositiveIntegerField(default=0)
    is_online=models.PositiveIntegerField(default=0)  #0-offline, 1-online, 2-resume
    is_engaged = models.BooleanField(default=False)


    # exit_time = models.DateTimeField(default=datetime.now)    #not used
    # offline_duration = models.PositiveIntegerField(default=0) #not used

    share_code=models.CharField(default='',max_length=10)

    def __str__(self):
        return str(self.id)+self.name

class AppLink(models.Model):
    url = models.CharField(max_length=1000,blank=True,null=True)

    def __str__(self):
        return self.url

class UserContactList(models.Model):
    user = models.ForeignKey(RegisteredUser,on_delete=models.CASCADE, related_name='ucl_ruser')
    name = models.CharField(max_length=100, blank=True, null=True)
    contact_country_code = models.CharField(max_length=10,blank=True, null=True)
    contact_mobile = models.CharField(max_length=15, blank=True, null=True)
    contact_status = models.CharField(max_length=20, choices = contact_status)

    def __str__(self):
        return str(self.user.name) + '---' + self.name


######## NEW CODE ########


friend_status=(('1','waiting'),('2','accepted'),('3','declined'))
class UserFriendList(models.Model):
    player=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='f_user',null=True)
    friend=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='f_friend', null=True)
    status=models.CharField(max_length=50,choices=friend_status,default='1')
    created_on=models.DateTimeField(auto_now=True)
    def __str__(self):
        return 'user-'+str(self.player.id)+'-friend-'+str(self.friend.id)

class Group(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    number_of_players = models.PositiveIntegerField(default=2)
    created_by = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, related_name="gr1_ruser")
    created_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class GroupJoinedMembers(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="gm1_group")
    ruser = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, related_name='gm1_ruser')
    joined_on = models.DateTimeField(auto_now_add=True)
    # reference = models.ForeignKey(RegisteredUser,on_delete=models.CASCADE, related_name='gm1_reference', null=True)
    # is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.group.name + '---' + self.ruser.name

# from solo.models import Game
friend_status=(('1','waiting'),('2','accepted'),('3','declined'))
class GameRequestList(models.Model):
    grto=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='gr_user')
    grfrom=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='gr_friend')
    # game=models.ForeignKey(Game,on_delete=models.CASCADE,related_name='gr_game')
    status=models.CharField(max_length=50,choices=friend_status,default='1')
    created_on=models.DateTimeField(auto_now=True)
    def __str__(self):
        return 'user-'+str(self.grto.id)+'-friend-'+str(self.grfrom.id)

notification_status=(('1','active'),('2','inactive'),('3','expired'))
req_type=(('1','game request'),('2','join group request'),('3','other'),('4','friend request'),('5','from admin'))
class UserNotification(models.Model):
    notification=models.CharField(max_length=500,null=True,blank=True)
    user=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='n_user')
    created_on=models.DateTimeField(auto_now=True)
    req_type=models.CharField(max_length=50,choices=req_type,default='1')
    ref_id=models.CharField(max_length=100,default='')
    status=models.CharField(max_length=50,choices=notification_status,default='1')
    def __str__(self):
        return self.user.name+'--'+self.notification
