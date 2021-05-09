from django.db.models import Count
from django.db.models import Q
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.renderers import JSONRenderer
from django.core import serializers
from django.contrib.auth.models import User
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from estacioMedioambientalApp.serializers import ClientSerializer, SensorSerializer, RegistreSerializer, SensorTypeSerializer, LocationSerializer, RegistreMovilSerializer
from estacioMedioambientalApp.models import Client, Sensor, Registre, SensorType, Location, RegistreMovil
import json
from rest_framework import viewsets
from django.http import JsonResponse
from django.views.generic.base import View
from django.shortcuts import render
import reverse_geocode
from django.utils.crypto import get_random_string

################### API #####################


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorTypeViewSet(viewsets.ModelViewSet):
    queryset = SensorType.objects.all()
    serializer_class = SensorTypeSerializer


class RegistreViewSet(viewsets.ModelViewSet):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    queryset = Registre.objects.all()
    serializer_class = RegistreSerializer


class Paisos(APIView):

    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        valors = [pais for pais in Location.objects.all().values(
            'pais').distinct()]
        return Response(valors)


class LocalitzacioPerPais(APIView):

    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """

        valors = [pais for pais in Location.objects.all().values(
            'pais').distinct()]
        return Response(valors)


class AllLocalitzacions(APIView):

    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """

        serializer = LocationSerializer(
            Location.objects.all(), many=True)
        return Response(serializer.data)


class ListRegistres(APIView):

    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        # valors = [Registre.valor for Registre in Registre.objects.all()]

        # serializer = LocationSerializer(
        #     Location.objects.all().values('pais').distinct(), many=True)
        valors = [pais for pais in Location.objects.all().values(
            'pais').distinct()]
        # token = Token.objects.create(user=User.objects.filter())
        return Response(valors)


class GetSensorTypes(APIView):

    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Retorna una llista de tots els .
        """
        serializer = SensorTypeSerializer(SensorType.objects.all(), many=True)
        return Response(serializer.data)


class ValuesFromClient(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Retorna una llista de tots els .
        """
        idClient = request.GET.get('id')
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        client = Client.objects.filter(id=idClient, actiu=True).first()
        if client.usuari != user:
            return Response("El client no es de la teva propietat", status=status.HTTP_404_NOT_FOUND)

        typusDeSensors = SensorType.objects.all()
        resultatFinal = {}
        for typusSensor in typusDeSensors:
            # Agafo tots els sensors dels clients de la ciutat demanada i amb el tipus concret
            sensors = Sensor.objects.filter(
                client=idClient, tipusSensor=typusSensor)

            if sensors:
                # Llistare els sensors com a filtres de els registres
                filtreRegistresClient = Q()
                for sensor in sensors:
                    filtreRegistresClient = filtreRegistresClient | Q(
                        sensor=sensor)

                # Agafare tots els registres de aqueslls sensors de la ciutat que no estiguin en quarentena
                registres = Registre.objects.filter(filtreRegistresClient)

                registresMovils = RegistreMovil.objects.filter(
                    filtreRegistresClient)

                llistaRegistres = []

                for registre in registres:
                    llistaRegistres.append(registre)

                for registreMovil in registresMovils:
                    registreTemporal = Registre()
                    registreTemporal.sensor = registreMovil.sensor
                    registreTemporal.valor = registreMovil.valor
                    registreTemporal.hora = registreMovil.hora
                    llistaRegistres.append(registreTemporal)
                    pass

                resultatFinal[typusSensor.toJSON()] = RegistreSerializer(
                    llistaRegistres, many=True).data

        # serializer = SensorTypeSerializer(SensorType.objects.all(), many=True)
        return Response(resultatFinal)


class GetClientsFromUser(APIView):
    """
    high level support for doing this and that.
    """

    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Retorna una llista de tots els .
        """
        # user = Token.objects.get(key=authentication.TokenAuthentication).user
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        serializer = ClientSerializer(
            Client.objects.filter(usuari=user_id, actiu=True), many=True)
        return Response(serializer.data)


class login(APIView):

    # permission_classes = [permissions.IsAdminUser]

    def post(self, request, format=None):
        """
        Retorna una llista de tots els .
        """
        # user = Token.objects.get(key=authentication.TokenAuthentication).user
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        serializer = ClientSerializer(
            Client.objects.filter(usuari=user_id, actiu=True), many=True)
        return Response(serializer.data)


class GetClient(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Retorna el client per el id demanat
        """
        # user = Token.objects.get(key=authentication.TokenAuthentication).user
        idClient = request.GET.get('id')
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        client = Client.objects.filter(id=idClient, actiu=True).first()
        if client.usuari != user:
            return Response("El client no es de la teva propietat", status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ClientSerializer(client)
            return Response(serializer.data)


class Locations(APIView):

    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        pais = request.GET.get('pais')
        # valors = [Registre.valor for Registre in Registre.objects.all()]

        clients = Client.objects.all()

        if not clients:
            return Response("No hi ha clients en la base de dades", status=status.HTTP_404_NOT_FOUND)

        filtreClients = Q()
        for client in clients:
            filtreClients = filtreClients | Q(id=client.localitzacio.id)

        if(pais):

            registresMovils = RegistreMovil.objects.filter(pais=pais)
            filtreRegistresMovils = Q()
            for registreMovil in registresMovils:
                filtreClients = filtreClients | Q(
                    id=registreMovil.localitzacio.id)

            filtreClients = filtreClients & Q(pais=pais)
            serializer = LocationSerializer(
                Location.objects.filter(filtreClients), many=True)

        else:

            registresMovils = RegistreMovil.objects.all()
            for registreMovil in registresMovils:
                filtreClients = filtreClients | Q(
                    id=registreMovil.localitzacio.id)

            serializer = LocationSerializer(
                Location.objects.filter(filtreClients), many=True)
        return Response(serializer.data)


class DataByCity(APIView):

    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        # Comprovacions de la peticio
        ciutat = request.GET.get('ciutat')
        pais = request.GET.get('pais')
        # sensorType = request.GET.get('sensor')

        if not ciutat:
            return Response("No hi ha ciutat", status=status.HTTP_404_NOT_FOUND)

        if not pais:
            return Response("No hi ha pais", status=status.HTTP_404_NOT_FOUND)

        # if not sensorType:
        #    return Response("No hi ha tipus de sensor", status=status.HTTP_404_NOT_FOUND)

        # Agafo localitzacio correcte
        location = Location.objects.filter(pais=pais, localitat=ciutat).first()

        # Comprovo que la localitzacio sigui valida
        if not location:
            return Response("No es una localitzacio valida", status=status.HTTP_404_NOT_FOUND)

        # Agafo els clients de aquella localitzacio i que no estiguin en quarentena
        clients = Client.objects.filter(
            localitzacio=location, quarentena=False)

        clientsMovils = Client.objects.filter(movil=True, quarentena=False)

        resistresMovils = RegistreMovil.objects.filter(localitzacio=location)

        # Comprovo que hi hagin clients valids
        if not clients and not resistresMovils:
            return Response("No hi han clients en aquesta localitat o els que hi han estan en quarentena", status=status.HTTP_404_NOT_FOUND)

        # Els llisto com a filtres dels sensors
        filtreSensorClient = Q()
        for client in clients:
            filtreSensorClient = filtreSensorClient | Q(client=client)

        filtreSensorClientMovils = Q()
        for clientMovil in clientsMovils:
            filtreSensorClientMovils = filtreSensorClientMovils | Q(
                client=clientMovil)

        # Agafare els typus de sensors per crear un dicionari amb el nom del sensor
        typusDeSensors = SensorType.objects.all()
        resultatFinal = {}
        for typusSensor in typusDeSensors:
            # Agafo tots els sensors dels clients de la ciutat demanada i amb el tipus concret
            sensors = None
            if clients:
                sensors = Sensor.objects.filter(
                    filtreSensorClient, tipusSensor=typusSensor)

            sensorsMovils = None
            if clientsMovils:
                sensorsMovils = Sensor.objects.filter(
                    filtreSensorClientMovils, tipusSensor=typusSensor)

            if sensors and sensorsMovils:

                # Llistare els sensors com a filtres de els registres
                filtreRegistresClient = Q()
                for sensor in sensors:
                    filtreRegistresClient = filtreRegistresClient | Q(
                        sensor=sensor)

                filtreRegistresClientMovil = Q()
                for sensorMovil in sensorsMovils:
                    filtreRegistresClientMovil = filtreRegistresClientMovil | Q(
                        sensor=sensorMovil)

                # Agafare tots els registres de aqueslls sensors de la ciutat que no estiguin en quarentena
                registres = Registre.objects.filter(filtreRegistresClient)

                registresMovils = RegistreMovil.objects.filter(
                    filtreRegistresClientMovil, localitzacio=location)

                llistaRegistres = []

                for registre in registres:
                    llistaRegistres.append(registre)

                for registreMovil in registresMovils:
                    registreTemporal = Registre()
                    registreTemporal.sensor = registreMovil.sensor
                    registreTemporal.valor = registreMovil.valor
                    registreTemporal.hora = registreMovil.hora
                    llistaRegistres.append(registreTemporal)
                    pass

                resultatFinal[typusSensor.toJSON()] = RegistreSerializer(
                    llistaRegistres, many=True).data
                # return Response(resultatFinal)

            elif sensors:
                # Llistare els sensors com a filtres de els registres
                filtreRegistresClient = Q()
                for sensor in sensors:
                    filtreRegistresClient = filtreRegistresClient | Q(
                        sensor=sensor)

                registres = Registre.objects.filter(filtreRegistresClient)

                resultatFinal[typusSensor.toJSON()] = RegistreSerializer(
                    registres, many=True).data

            elif sensorsMovils:
                filtreRegistresClientMovil = Q()
                for sensorMovill in sensorsMovils:
                    filtreRegistresClientMovil = filtreRegistresClientMovil | Q(
                        sensor=sensorMovill)

                registresMovils = RegistreMovil.objects.filter(
                    filtreRegistresClientMovil, localitzacio=location)

                resultatFinal[typusSensor.toJSON()] = RegistreMovilSerializer(
                    registresMovils, many=True).data

                pass
        # Serialitzare els registres amb el serialitzado de django
        # serializer = RegistreSerializer(registres, many=True)

        return Response(resultatFinal)


class TestApi(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Prova per python
        """

        coordinates = (41.4500447, 2.2474122)
        # reverse_geocode.search(coordinates)
        # location.raw
        # return Response(request.data)
        return Response(request.data)

    def post(self, request, format=None):
        """
        Prova per python
        """

        return Response(request.data)
        # return Response("bon post crack")


class AddStaticData(APIView):

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Prova 
        """

        # return Response(request.data)
        return Response("Ok mister")

    def post(self, request, format=None):
        """
        Prova per python
        """

        # coordinates = (request.data["lat"], request.data["long"])
        # return Response(reverse_geocode.get(coordinates))

        if not "hora" in request.data:
            return Response("Es necesari enviar la hora de presa de dades", status=status.HTTP_404_NOT_FOUND)

        if not "token" in request.data:
            return Response("Es necesari enviar un token", status=status.HTTP_404_NOT_FOUND)

        client = Client.objects.filter(token=request.data["token"]).first()

        if not client:
            return Response("El client no es valid", status=status.HTTP_404_NOT_FOUND)

        if not client.movil:

            for key, dada in request.data["data"].items():
                sensorActual = Sensor.objects.filter(
                    client=client, identificador=key).first()
                if sensorActual:
                    Registre.objects.create(
                        hora=request.data["hora"], valor=str(dada), sensor=sensorActual)

            return Response("Les dades s'han introduit correctament", status=status.HTTP_200_OK)

        else:
            if not "lat" in request.data or not "long" in request.data:
                return Response("Es necesari enviar la latitud i longitud", status=status.HTTP_404_NOT_FOUND)

            coordinates = (request.data["lat"], request.data["long"])
            posibleLocalitzacio = reverse_geocode.get(coordinates)
            localitzacio = Location.objects.filter(
                pais=posibleLocalitzacio["country"], localitat=posibleLocalitzacio["city"]).first()

            if localitzacio:

                for key, dada in request.data["data"].items():
                    sensorActual = Sensor.objects.filter(
                        client=client, identificador=key).first()
                    if sensorActual:
                        #                       RegistreMovil.objects.create(hora=request.data["hora"], valor=dada[key], localitzacio=localitzacio, latitudReal=float(request.data["lat"]), longitudReal=float(request.data["long"]), sensor=sensorActual)
                        RegistreMovil.objects.create(hora=request.data["hora"], valor=str(
                            dada), localitzacio=localitzacio, latitudReal=5.7, longitudReal=7.4, sensor=sensorActual)

                return Response("Les dades s'han afegit correctament en una localitzacio existent", status=status.HTTP_200_OK)

            else:

                localitzacioCrear = Location.objects.create(
                    pais=posibleLocalitzacio["country"], localitat=posibleLocalitzacio["city"], latitud=request.data["lat"], longitud=request.data["long"], altitud=0)
                for key, dada in request.data["data"].items():
                    sensorActual = Sensor.objects.filter(
                        client=client, identificador=key).first()
                    if sensorActual:
                        RegistreMovil.objects.create(hora=request.data["hora"], valor=str(
                            dada), localitzacio=localitzacioCrear, latitudReal=request.data["lat"], longitudReal=equest.data["long"], sensor=sensorActual)

                return Response("Les dades s'han afegit correctament en una localitzacio creada", status=status.HTTP_200_OK)

        # return Response("bon post crack")


class deleteClient(APIView):
    """
    Prova per python
    """
    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def post(self, request, format=None):
        """
        Prova per python
        """

        clientPerEliminar = Client.objects.filter(
            id=request.data["id"]).first()
        clientPerEliminar.actiu = False
        clientPerEliminar.save()
        return Response(request.data)
        # return Response("bon post crack")


class register(APIView):
    """
    Prova per python
    """
    #authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def post(self, request, format=None):
        """
        Prova per python
        """

        user = User.objects.create_user(
            username=request.data["user"], password=request.data["password"])

        token = Token.objects.create(user=user)
        print(token)

        return Response(str(token))
        # return Response("bon post crack")


class AddClientExistentLocation(APIView):
    """
    Prova per python
    """
    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def post(self, request, format=None):
        """
        Prova per python
        """

        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        print(request.data['sensors'])
        token = get_random_string(length=32)

        location = Location.objects.filter(
            id=request.data["location"]).first()

        client = Client.objects.create(
            usuari=user, identificador=request.data["name"], token=token, actiu=True, movil=True, localitzacio=location, quarentena=True)

        for sensor in request.data["sensors"]:
            sensor = Sensor.objects.create(
                identificador=sensor['name'], tipusSensor=SensorType.objects.get(id=sensor['type']), client=client)

        return Response(client.id)
        # return Response("bon post crack")


class AddClientNewLocation(APIView):
    """
    Prova per python
    """
    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def post(self, request, format=None):
        """
        Prova per python
        """

        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        print(request.data['sensors'])
        token = get_random_string(length=32)

        coordinates = (request.data["lat"], request.data["long"])
        posibleLocalitzacio = reverse_geocode.get(coordinates)
        localitzacio = Location.objects.filter(
            pais=posibleLocalitzacio["country"], localitat=posibleLocalitzacio["city"]).first()

        if localitzacio:
            client = Client.objects.create(
                usuari=user, identificador=request.data["name"], token=token, actiu=True, movil=True, localitzacio=localitzacio, quarentena=True)

            for sensor in request.data["sensors"]:
                sensor = Sensor.objects.create(
                    identificador=sensor['name'], tipusSensor=SensorType.objects.get(id=sensor['type']), client=client)

            return Response(client.id)

        else:

            localitzacioCrear = Location.objects.create(
                pais=posibleLocalitzacio["country"], localitat=posibleLocalitzacio["city"], latitud=request.data["lat"], longitud=request.data["long"], altitud=0)

            client = Client.objects.create(
                usuari=user, identificador=request.data["name"], token=token, actiu=True, movil=True, localitzacio=localitzacioCrear, quarentena=True)

            for sensor in request.data["sensors"]:
                sensor = Sensor.objects.create(
                    identificador=sensor['name'], tipusSensor=SensorType.objects.get(id=sensor['type']), client=client)

            return Response(client.id)

            # return Response("bon post crack")


class AddClientMovil(APIView):
    """
    Prova per python
    """
    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def post(self, request, format=None):
        """
        Prova per python
        """

        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        print(request.data['sensors'])
        token = get_random_string(length=32)
        location = Location.objects.filter(
            localitat="none", pais="none").first()
        client = Client.objects.create(
            usuari=user, identificador=request.data["name"], token=token, actiu=True, movil=True, localitzacio=location, quarentena=True)

        for sensor in request.data["sensors"]:
            sensor = Sensor.objects.create(
                identificador=sensor['name'], tipusSensor=SensorType.objects.get(id=sensor['type']), client=client)

        return Response(client.id)
        # return Response("bon post crack")
