from rest_framework import serializers
from extra.models import *

class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model=AboutUs
        fields='__all__'

class TermsAndConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model=TermsAndCondition
        fields='__all__'

class LegalSerializer(serializers.ModelSerializer):
    class Meta:
        model=Legal
        fields='__all__'
