from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cabinet, Guest
from .serializers import GuestSerializer, CabinetSerializer


class CabinetViewSet(viewsets.ModelViewSet):

    serializer_class = CabinetSerializer
    queryset = Cabinet.objects.all()
    
    @action(detail=False)
    def all_guests(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def empty_guest(self, request):
        Guest.objects.create(number=-1,tg_id=-1,cabinets='')
        return Response('Empty guest created')
        
        