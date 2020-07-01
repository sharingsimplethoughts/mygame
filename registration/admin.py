from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(CountryCode)
admin.site.register(LevelType)
admin.site.register(Level)
admin.site.register(RegisteredUser)
admin.site.register(UserContactList)
admin.site.register(AppLink)
admin.site.register(UserFriendList)
admin.site.register(GameRequestList)
admin.site.register(UserNotification)
admin.site.register(Group)
admin.site.register(GroupJoinedMembers)