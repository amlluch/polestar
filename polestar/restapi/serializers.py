from rest_framework import serializers
from .models import Csv, Ships, Positions
from rest_framework.validators import UniqueValidator

import re

class UploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Csv
        fields = ('csvfile',)
        write_only_fields = ('csvfile',)

    def validate_csvfile(self, obj):
        pattern = re.compile('^([a-zA-Z0-9\s_\\.\-\(\):])+(.csv)+$')
        if pattern.match(obj.name):
            return super(UploadSerializer, self).validate(obj)
        else:
            raise serializers.ValidationError('Only csv files admitted')

    def create(self, validated_data):
        return Csv.objects.create(**validated_data)

class ShipsSerializer(serializers.ModelSerializer):

    imo = serializers.CharField(required = True, validators=[UniqueValidator(queryset=Ships.objects.all())])

    class Meta:
        model = Ships
        fields = ('imo', 'name')
        write_only_fields = ('imo', 'name')
    
    def validate_imo(self, value):
        pattern = re.compile('^(\d{7})+$')
        if pattern.match(value):
            return super(ShipsSerializer, self).validate(value)
        else:
            raise serializers.ValidationError('The ship code must consist of 7 numbers')

    def create(self, validated_data):
        return Ships.objects.create(**validated_data)

class PositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Positions
        fields = ('timestamp', 'latitude', 'longitude')