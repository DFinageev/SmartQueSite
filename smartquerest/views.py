from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cabinet, Guest
from .serializers import GuestSerializer, CabinetSerializer
import json


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
        
    @action(detail=False, methods=['post'])
    def create_guest(self, request):
        guests = Guest.objects.all().order_by('-number')
        number = guests[0].number + 1
        cabs_names = json.loads(request.POST['json_s'])
        print(cabs_names)
        cabs = Cabinet.objects.all().filter(cab_name__in=cabs_names)
        print(cabs)
        #jsreq = json.loads(request)
        Guest.objects.create(number=number,tg_id=-1,cabinets=' '.join([str(x) for x in cabs.values_list('cab_number', flat=True)]))
        return Response(f'{number}')
        
    @action(detail=False)
    def cabinets_by_name(self, request):
        cabs = Cabinet.objects.values_list('cab_name', flat=True)
        cabsdata = {'cabs' : list(cabs)}
        jsoncabs = json.dumps(cabsdata)
        return Response(jsoncabs)
    
    #@action(detail=False)
    #def check_cabinet_key(self, request):
        