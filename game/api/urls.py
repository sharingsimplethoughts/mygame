from django.urls import path
from .views import *
app_name='game'

urlpatterns = [
    path('save_room_password',SaveRoomPassView.as_view(),name='g_save_password'),
    path('get_room_password',RoomPassListView.as_view(),name='g_get_room_password'),
]
