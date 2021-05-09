"""estacioMedioambiental URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views


######## API #########
from estacioMedioambientalApp.views import ClientViewSet, SensorViewSet, RegistreViewSet, SensorTypeViewSet

######## APIViews #########
from estacioMedioambientalApp.views import ListRegistres, Paisos, LocalitzacioPerPais, Locations, DataByCity, GetSensorTypes, GetClientsFromUser, GetClient, ValuesFromClient, login, TestApi, AllLocalitzacions, AddStaticData, deleteClient, register, AddClientExistentLocation, AddClientNewLocation, AddClientMovil


class ApiDeLaEstacioMeteorologica(routers.APIRootView):
    """
    Api de la estacio meteorologica
    """
    pass


class DocumentedRouter(routers.DefaultRouter):
    APIRootView = ApiDeLaEstacioMeteorologica


router = DocumentedRouter()

#router = routers.DefaultRouter()
router.register('Clients', ClientViewSet)
router.register('Sensors', SensorViewSet)
router.register('Registre', RegistreViewSet)
router.register('SensorType', SensorTypeViewSet)


urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('', include('pwa.urls')),

    ###### API ######
    path('docs/', include_docs_urls(title='Django', public=False)),
    path('api/', include(router.urls)),

    ##### APIViews ######
    path('api/GetClient', GetClient.as_view()),
    path('api/AddData', AddStaticData.as_view()),
    path('api/Paisos', Paisos.as_view()),
    path('api/AllLocalitzacions', AllLocalitzacions.as_view()),
    path('api/test', TestApi.as_view()),
    path('api/api-token-auth/', views.obtain_auth_token),
    path('api/login', login.as_view()),
    path('api/ValuesFromClient', ValuesFromClient.as_view()),
    path('api/clients', GetClientsFromUser.as_view()),
    path('api/AllCountries', ListRegistres.as_view()),
    path('api/LocationForCountry', LocalitzacioPerPais.as_view()),
    path('api/Locations', Locations.as_view()),
    path('api/DataByCity', DataByCity.as_view()),
    path('api/GetSensorTypes', GetSensorTypes.as_view()),
    path('api/deleteClient', deleteClient.as_view()),
    path('api/register', register.as_view()),
    path('api/AddClient/ExistentLocation', AddClientExistentLocation.as_view()),
    path('api/AddClient/NewLocation', AddClientNewLocation.as_view()),
    path('api/AddClient/Movil', AddClientMovil.as_view()),

]
