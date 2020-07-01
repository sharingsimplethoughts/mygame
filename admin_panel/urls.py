from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.conf.urls import url,include

urlpatterns = [


    # api for admin panel

    path('login/', AdminLoginView.as_view(),name='admin-login'),
    path('home/', login_required(AdminHomeView.as_view()),name='admin-home'),
    path('logout/',LogoutView.as_view(),name='admin-logout'),

    # password reset by mail

    url(r'^password_reset/$', ResetPasswordView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView, name='password_reset_complete'),

    # change password
    path('change_password/', login_required(ChangePasswordView.as_view()), name='admin-change-password'),

    # admin profile
    path('admin_profile/', login_required(AdminProfileView.as_view()), name='admin-profile'),
    path('admin_profile/edit', login_required(AdminProfileEditView.as_view()), name='admin-profile-edit'),

    # account management


]