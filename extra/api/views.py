from rest_framework.views import (APIView)
from extra.models import *
from .serializers import *
import logging
logger = logging.getLogger('accounts')

class TermsAndCondition(APIView):
    def get(self,request,*args,**kwargs):
        logger.debug('Terms and condition get called')
        logger.debug(request.data)
        queryset=TermsAndCondition.objects.all().first()
        data=TermsAndConditionSerializer(queryset).data
        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=200,)

class AboutUs(APIView):
    def get(self,request,*args,**kwargs):
        logger.debug('About us get called')
        logger.debug(request.data)
        queryset=AboutUs.objects.all().first()
        data=AboutUsSerializer(queryset).data
        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=200,)

class Legal(APIView):
    def get(self,request,*args,**kwargs):
        logger.debug('Legal get called')
        logger.debug(request.data)
        queryset=Legal.objects.all().first()
        data=LegalSerializer(queryset).data
        return Response({
            'message':'data retrieved successfully',
            'success':'True',
            'data':data,
        },status=200,)
