from rest_framework import serializers
from django.db.models import Max
from rest_framework.exceptions import APIException
from game.models import *

class SaveRoomPassSerializer(serializers.ModelSerializer):
    room_name=serializers.CharField(allow_blank=True)
    room_pass=serializers.CharField(allow_blank=True)
    class Meta:
        model = TemporaryStorage
        fields = ('room_name','room_pass')

    def validate(self,data):
        room_name=data['room_name']
        room_pass=data['room_pass']
        if not room_name or room_name=="":
            raise APIException('Please provide room name')
        if not room_pass or room_pass=="":
            raise APIException('Please provide room pass')
        return data
    def create(self,validated_data):
        room_name=validated_data['room_name']
        room_pass=validated_data['room_pass']
        ts = TemporaryStorage(
            room_name=room_name,
            room_pass=room_pass,
        )
        ts.save()
        return validated_data

class RoomPassListSerializer(serializers.ModelSerializer):
    class Meta:
        model=TemporaryStorage
        fields = '__all__'
        