from rest_framework import serializers

from .models import Guest
from .models import Cabinet
#from .models import Schedule


class CabinetSerializer(serializers.Serializer):
    cab_number = serializers.IntegerField()
    cab_name = serializers.CharField(max_length=255)
    tg_id = serializers.IntegerField(default=-1)
    key = serializers.IntegerField()
    query = serializers.CharField()
    
    def create(self, validated_data):
        return Cabinet.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.cab_number = validated_data.get('cab_number', instance.cab_number)
        instance.cab_name = validated_data.get('cab_name', instance.cab_name)
        instance.tg_id = validated_data.get('tg_id', instance.tg_id)
        instance.key = validated_data.get('key', instance.key)
        instance.query = validated_data.get('query', instance.query)
        instance.save()
        return instance


class GuestSerializer(serializers.Serializer):
    number = serializers.IntegerField()
    tg_id = serializers.IntegerField()
    cabinets = serializers.CharField()
    cabinet = CabinetSerializer()
    
    def create(self, validated_data):
        return Guest.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.number = validated_data.get('number', instance.number)
        instance.tg_id = validated_data.get('tg_id', instance.tg_id)
        instance.cabinets = validated_data.get('cabinets', instance.cabinets)
        instance.save()
        return instance
    

class MovedGuestSerializer(serializers.Serializer):
    guest_key = serializers.IntegerField()
    
    def create(self, validated_data):
        return MovedGuest.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.guest_key = validated_data.get('guest_key', instance.guest_key)
        instance.save()
        return instance
'''
class ScheduleSerializer(serializers.Serializer):
    query = CabinetSerializer(read_only=True, many=True)
    
    def create(self, validated_data):
        return Schedule.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.query = validated_data.get('query', instance.query)
        instance.save()
        return instance
'''