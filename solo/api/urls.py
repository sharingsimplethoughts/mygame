from django.urls import path
from .views import *

app_name='solo'

urlpatterns=[
    path('hand_list/',HandListView.as_view(),name='hand_list'),
    path('coin_list/',CoinListView.as_view(),name='coin_list'),
    # path('create_room/',CreateRoomView.as_view(),name='create_room'),
    # path('update_room_manager/',UpdateBeforeGameStartView.as_view(),name='update_before_game_start'),
    # path('submit_game_round/',SubmitSoloGameRoundView.as_view(),name='solo_submit_game_round'),

    path('game_start/',GameStartView.as_view(),name='game_start'),
    path('game_end/',GameEndView.as_view(),name='game_end'),
]
