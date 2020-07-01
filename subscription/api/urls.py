from django.urls import path
from .views import *

app_name="subscription"

urlpatterns = [
    path('subscription_plan_list/',SubscriptionPlanListView.as_view(),name='subscription_plan_list'),
    path('subscribe/',UserSubscribeView.as_view(),name="subscribe"),

]
