from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticated,)
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from rest_framework.response import Response
from solo.models import *
from registration.models import *
from subscription.models import *
from .serializers import *
import logging
logger = logging.getLogger('accounts')

class SubscriptionPlanListView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def get(self,request,*args,**kwargs):
        queryset = SubscriptionPlan.objects.filter(is_blocked=False)
        serializer = SubscriptionPlanListSerializer(queryset,many=True,context={'request':request})
        if serializer:
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data,
            },status=200)
        return Response({
            'message':'Data retrieve failed',
            'success':'False'
        },status=400)

class UserSubscribeView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def post(self,request,*args,**kwargs):
        pass
        # user=request.user
        # serializer=
    