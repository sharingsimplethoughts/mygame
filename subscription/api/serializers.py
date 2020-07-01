from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from django.db.models import Max
from registration.models import *
from subscription.models import *
import string
import random
from rest_framework.exceptions import APIException

class SubscriptionPlanListSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubscriptionPlan
        fields=('id','name','amount','validity',)


