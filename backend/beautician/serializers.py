from rest_framework.serializers import ModelSerializer
from .models import *


class BeauticianSerializer(ModelSerializer):
    class Meta:
        model=Beautician
        fields= "__all__"


class ServicesSerializer(ModelSerializer):
    class Meta:
        model=Services
        fields= "__all__"

class StudioSerializer(ModelSerializer):
    class Meta:
        model=Studio
        fields= "__all__"

class ServicefeesSerializer(ModelSerializer):
    service=ServicesSerializer()
    beautician=BeauticianSerializer()
    class Meta:
        model=Servicefees
        fields= "__all__"

