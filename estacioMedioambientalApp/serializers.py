from rest_framework import serializers
from estacioMedioambientalApp.models import Client, Sensor, Registre, SensorType, Location, RegistreMovil


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = [
            'id',
            'identificador',
            'localitzacio',
            'quarentena',
            'dataQuarentena',
            'getQuantSensors',
            'getLocation',
            'token',
            'movil',
            'getSensors'
        ]


class SensorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sensor
        fields = [
            'identificador',
            'client',
            'tipusSensor'
        ]


class RegistreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registre
        fields = [
            'hora',
            'valor',
            'sensor'
        ]


class RegistreMovilSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegistreMovil
        fields = [
            'hora',
            'valor',
            'sensor'
        ]


class SensorTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SensorType
        fields = [
            'id',
            'tipus',
            'unitatMesura',
            'valorMaximPotable',
            'valorMinimPotable',
            'descripcio',
            'valorMaxim',
            'valorMinim',
        ]


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = [
            "id",
            'pais',
            'localitat',
            'latitud',
            'longitud',
            "altitud"
        ]
