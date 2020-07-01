from django.urls import path

from .views import *
app_name='registration'

urlpatterns=[
    path('register/',RegistrationView.as_view(),name='register'),
    path('nationality_list/',CountryCodeListView.as_view(),name='nationality_list'),
    path('countrycode_list/',CountryCodeListView.as_view(),name='countrycode_list'),
    path('add_contact_list/',AddContactListView.as_view(),name='add_contact_list'),
    path('add_link/',AddAppLinkView.as_view(),name='add_link'),
    path('send_invitation/',SendInvitationView.as_view(),name='send_invitation'),
    path('search_country/',SearchCountry.as_view(),name='send_invitation'),
    path('get_screen_5/',Screen_5_View.as_view(),name='get_screen_5'),
    path('get_screen_10/',Screen_10_View.as_view(),name='get_screen_10'),
    path('user_detail/',UserDetailView.as_view(),name='user_detail'),
    path('only_profile_image/',OnlyProfileImageView.as_view(),name='only_profile_image'),
    # path('update_invitation/',UpdateInvitationView.as_view(),name='update_invitation'), #already done in registration serializer
    path('get_user_detail_based_on_id/',UserDetailBasedOnIdView.as_view(),name='get_user_detail_based_on_id'),
    path('multiple_user_detail/',MultipleUserDetailView.as_view(),name='multiple_user_detail'),

    path('send_request/',SendRequestView.as_view(),name='send_game_request'),
    path('get_notification_list/',GetNotificationListView.as_view(),name='get_notification_list'),
    path('accept_request/',AcceptRequestView.as_view(),name='accept_game_request'),
    path('decline_request/',DeclineRequestView.as_view(),name='decline_game_request'),
    # path('send_general_notification/',SendGeneralNotificatonView.as_view(),name='send_general_notification'),

    path('get_share_code/',GetShareCodeView.as_view(),name='get_share_code'),
    path('get_friend_list/',GetFriendListView.as_view(),name='get_friend_list'),

    path('create_group/',CreateGroupView.as_view(),name='create_group'),
    path('get_group_members/<int:pk>',GetGroupMembersListView.as_view(),name='get_group_members'),
    path('get_all_group_list/',GetAllGroupListView.as_view(),name='get_all_group_list'),
    path('get_created_group_list/',GetCreatedGroupListView.as_view(),name='get_all_group_list'),
    path('get_joined_group_list/',GetJoinedGroupListView.as_view(),name='get_all_group_list'),
    path('search_user_by_name_or_email/',GetUserBySearchView.as_view(),name='search_user_by_username_or_email'),

    path('remove_player_by_admin/',RemovePlayerByAdminView.as_view(),name='remove_player_by_admin'),
    path('remove_player_by_own/',RemovePlayerByOwn.as_view(),name='remove_player_by_own'),
    path('admin_exit/',AdminExitView.as_view(),name='admin_exit'),

    path('edit_profile/',EditProfileView.as_view(),name='edit_profile'),
]
