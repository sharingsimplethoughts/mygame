from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticated,)
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from rest_framework.response import Response
from game.models import *
from .serializers import *
import logging
logger = logging.getLogger('accounts')

class SaveRoomPassView(APIView):
    def post(self,request,*args, **kwargs):
        serializer = SaveRoomPassSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'data saved successfully',
                'success':'True'
            },status=200)
        return Response({
            'message':'data save failed',
            'success':'False'
        },status=400)

class RoomPassListView(APIView):
    def get(self,request,*args, **kwargs):
        queryset = TemporaryStorage.objects.all()
        serializer = RoomPassListSerializer(queryset,many=True,context={'request':request})
        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':serializer.data,
        })