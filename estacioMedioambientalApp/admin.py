from django.contrib import admin

from estacioMedioambientalApp.models import Client, Sensor, Registre, SensorType, Location, RegistreMovil

admin.site.site_header = "Estacio meteorologica"


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    # fields = ("usuari", "identificador", "localitzacio",
    #           "quarentena", "dataQuarentena")
    list_display = ("id", "usuari", "identificador", "localitzacio",
                    "quarentena", "dataQuarentena", "getQuantSensors", 'actiu', 'token', 'movil')
    search_fields = ("usuari__username", "identificador", "localitzacio",
                     "dataQuarentena", "quarentena", 'actiu', 'token')
    list_filter = ('actiu', 'quarentena', "usuari")

    # "getQuantClient"
    # list_display = ("identificador", "localitzacio")
    # pass


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ("id", "identificador", "tipusSensor", "client")
    list_filter = ("tipusSensor", )
    search_fields = ("identificador", "tipusSensor", "client")

    pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "pais", "localitat",
                    "latitud", "longitud", "altitud")
    list_filter = ("pais", )
    search_fields = ("pais", "localitat", "latitud", "longitud", "altitud")

    pass


@admin.register(Registre)
class RegistreAdmin(admin.ModelAdmin):
    list_display = ("id", 'valor', 'hora', 'sensor')
    search_fields = ('valor', 'hora', 'sensor')
    list_filter = ("hora", 'sensor')
    pass


@admin.register(RegistreMovil)
class RegistreMovilAdmin(admin.ModelAdmin):
    list_display = ("id", 'valor', 'hora', 'sensor', "localitzacio")
    search_fields = ('valor', 'hora', 'sensor', "localitzacio")
    list_filter = ("hora", 'sensor')
    pass


@admin.register(SensorType)
class SensorTypeAdmin(admin.ModelAdmin):
    list_display = ("id", 'tipus', 'unitatMesura',
                    'valorMaximPotable', 'valorMinimPotable', 'valorMaxim', 'valorMinim')
    search_fields = ('tipus', 'unitatMesura',
                     'valorMaximPotable', 'valorMinimPotable', 'valorMaxim', 'valorMinim')
    list_filter = ("tipus", "unitatMesura")

    pass
