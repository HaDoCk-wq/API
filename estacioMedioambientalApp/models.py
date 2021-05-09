from django.db import models
from django.contrib.auth.models import User
#from estacioMedioambientalApp.serializers import LocationSerializer

# Create your models here.


# class Usuari(AbstractUser):
#     loginToken = models.TextField((""))

class Location(models.Model):
    pais = models.TextField(("pais"))
    localitat = models.TextField(("localitat"))
    latitud = models.FloatField(("latitud"))
    longitud = models.FloatField(("longitud"))
    altitud = models.FloatField(("altitud"), null=True)

    def __str__(self):
        return f"{self.localitat}, {self.pais}"


class SensorType(models.Model):
    tipus = models.CharField(
        ("Tipus de sensor"), max_length=50)
    descripcio = models.TextField(("Breu descripcio"))
    unitatMesura = models.CharField(
        ("Unitat en la que mesura"), max_length=5)
    valorMaximPotable = models.FloatField(
        ("Valor maxim avans de que es consideri perillos"))
    valorMinimPotable = models.FloatField(
        ("Valor minim avans de que es consideri perillos"))
    valorMaxim = models.FloatField(("Valor maxim que s'acceptara com a valid"))
    valorMinim = models.FloatField(("Valor minim que s'acceptara com a valid"))

    def __str__(self):
        return f"{self.tipus} | {self.unitatMesura}"

    def toJSON(self):
        return '{"id": "' + str(self.id) + '", "tipus": "' + str(self.tipus) + '", "unitatMesura": "' + str(self.unitatMesura) + '", "valorMaximPotable": "' + str(self.valorMaximPotable) + '", "valorMinimPotable": "' + str(self.valorMinimPotable) + '" }'


class Client(models.Model):
    identificador = models.TextField(("Identificador"))
    token = models.TextField(("Token"))
    actiu = models.BooleanField(("Esta actiu"))
    movil = models.BooleanField(("Es movil"))
    localitzacio = models.ForeignKey("Location", verbose_name=(
        "Localitzacio"), on_delete=models.CASCADE, null=True, blank=True)
    quarentena = models.BooleanField(("Esta en quarentena"))
    dataQuarentena = models.DateTimeField(
        ("Inici de quarentena"), auto_now_add=True)
    usuari = models.ForeignKey(User, verbose_name=(
        "Propietari"), on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.identificador}, {self.localitzacio}"

    def getLocation(self):
        """
        Localitzacio
        """
        if self.localitzacio:
            return Location.objects.filter(id=self.localitzacio.id).values('pais', 'localitat').first()
        else:
            return None
    getLocation.short_description = 'Localitzacio del dispositiu'

    def getSensors(self):
        llista = {}
        for sensor in Sensor.objects.filter(client=self):
            llista[sensor.identificador] = SensorType.objects.filter(
                id=sensor.tipusSensor.id).values('tipus', 'unitatMesura').first()
        return llista
    getSensors.short_description = 'Agafa els sensors'

    def getQuantSensors(self):
        return Sensor.objects.filter(client=self).count()
    getQuantSensors.short_description = 'Quantitat de sensors'


class Sensor(models.Model):
    """
    Stores a single blog entry, related to :model:`Client`
    """
    identificador = models.TextField(("Identificador"))
    tipusSensor = models.ForeignKey("SensorType", verbose_name=(
        "Tipus de sensor"), on_delete=models.CASCADE)
    client = models.ForeignKey(
        Client, verbose_name=("Client pare"), on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return f"{self.identificador} | {self.tipusSensor}"


class Registre(models.Model):
    hora = models.DateTimeField(("Hora de dades"))
    valor = models.TextField(("Valor"))
    sensor = models.ForeignKey(
        Sensor, verbose_name=("Sensor"), on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return f"Val: {self.valor} | Sensor: {self.sensor}"


class RegistreMovil(models.Model):
    hora = models.DateTimeField(("Hora de dades"))
    valor = models.TextField(("Valor"))
    localitzacio = models.ForeignKey(
        Location, verbose_name=("Localitzacio"), on_delete=models.CASCADE, default=None, null=True)
    latitudReal = models.FloatField(("latitud"))
    longitudReal = models.FloatField(("longitud"))
    sensor = models.ForeignKey(
        Sensor, verbose_name=("Sensor"), on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return f"Val: {self.valor} | Sensor: {self.sensor}"
