from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticated,)
from rest_framework_jwt.authentication import  JSONWebTokenAuthentication
from rest_framework.response import Response
from solo.models import *
from .serializers import *
import logging
logger = logging.getLogger('accounts')

class HandListView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def get(self,request,*args,**kwargs):
        logger.debug('Hand list get called')
        logger.debug(request.data)
        queryset = Hand.objects.all()
        serializer=''
        if queryset.count() != 0:
            serializer = HandListSerializer(queryset, many=True, context={'request':request})
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data
            },status=200)
        else:
            return Response({
                'message':'Sorry no hand list available in database',
                'success':'False',                
            },status=400)

class CoinListView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def get(self,request,*args,**kwargs):
        logger.debug('Hand list get called')
        logger.debug(request.data)
        queryset = Coin.objects.all()
        if queryset.count() != 0:
            serializer = CoinListSerializer(queryset, many=True, context={'request':request})
            return Response({
                'message':'Data retrieved successfully',
                'success':'True',
                'data':serializer.data
            },status=200)
        else:
            return Response({
                'message':'Sorry no coin list available in database',
                'success':'False',
            },status=400)

class GameStartView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def post(self,request,*args,**kwargs):
        logger.debug('game start post called')
        logger.debug(request.data)
        user = request.user
        ruser = RegisteredUser.objects.filter(user=user).first()
        serializer = GameStartSerializer(data=request.data,context={'ruser':ruser})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Data updated successfully',
                'success':'True',
                'data':serializer.data
            },status=200,)
        return Response({
            'message':'Data update failed',
            'success':'False',
            'data':serializer.errors,
        },status=400,)

class GameEndView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(JSONWebTokenAuthentication,)
    def post(self,request,*args,**kwargs):
        logger.debug('game end post called')
        logger.debug(request.data)
        user = request.user
        ruser = RegisteredUser.objects.filter(user=user).first()
        serializer = GameEndSerializer(data=request.data,context={'ruser':ruser})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Data updated successfully',
                'success':'True',
                'data':serializer.data
            },status=200,)
        return Response({
            'message':'Data update failed',
            'success':'False',
            'data':serializer.errors,
        },status=400,)
        



# class UpdateBeforeGameStartView(APIView):
#     permission_classes=(IsAuthenticated,)
#     authentication_classes=(JSONWebTokenAuthentication,)
#     def post(self,request,*args,**kwargs):
#         logger.debug('Update before game post called')
#         logger.debug(request.data)
#         user = request.user
#         ruser = RegisteredUser.objects.filter(user=user).first()
#         serializer = UpdateBeforeGameStartSerializer(data=request.data,context={'ruser':ruser})
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 'message':'Data updated successfully',
#                 'success':'True',
#             },status=200,)
#         return Response({
#             'message':'Data update failed',
#             'success':'False',
#             'data':serializer.errors,
#         },status=400,)

# class SubmitSoloGameRoundView(APIView):
#     permission_classes=(IsAuthenticated,)
#     authentication_classes=(JSONWebTokenAuthentication,)
#     def post(self,request,*args,**kwargs):
#         logger.debug('Submit game round post called')
#         logger.debug(request.data)
#         serializer=SubmitSoloGameRoundSerializer(data=request.data,context={'request':request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 'message':'Data submited successfully',
#                 'success':'True',
#             },status=400,)
#         else:
#             return Response({
#                 'message':'Data submition failed',
#                 'success':'False',
#             },status=400,)

# class CreateRoomView(APIView):
#     permission_classes=(IsAuthenticated,)
#     authentication_classes=(JSONWebTokenAuthentication,)
#     def post(self,request,*args,**kwargs):
#         data=request.data
#         serializer=CreateRoomSerializer(data=data,context={'request':request})
#         if serializer.is_valid():
#             data=serializer.data
#             return Response({
#                 'message':'Room created successfully',
#                 'success':'True',
#                 'data':data,
#             },status=200,)
#         return Response({
#             'message':'Room creation failed',
#             'success':'False',            
#         },status=400,)

