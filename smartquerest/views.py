from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cabinet, Guest, MovedGuest
from .serializers import GuestSerializer, CabinetSerializer, MovedGuestSerializer
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
        return Response(json.dumps({
            "status" : "Empty guest created"
        }))
    
        
    @action(detail=False, methods=['post'])
    def create_guest(self, request):
        guests = Guest.objects.all().order_by('-number')
        number = guests[0].number + 1
        cabs_names = json.loads(request.POST['json_s'])
        print(cabs_names)
        cabs = Cabinet.objects.all().filter(cab_name__in=cabs_names)
        cabs_list = ' '.join([str(x) for x in cabs.values_list('cab_number', flat=True)])
        min_cab = cabs[0]
        min_len = len(Guest.objects.all().filter(cabinet=min_cab))
        for c in cabs:
            if len(Guest.objects.all().filter(cabinet=c)) < min_len:
                min_len = len(Guest.objects.all().filter(cabinet=c))
                min_cab = c
        #jsreq = json.loads(request)
        Guest.objects.create(number=number, tg_id=-1, cabinets=cabs_list, cabinet=min_cab)
        MovedGuest.objects.create(guest_key=number)
        print(number)
#        return Response(json.dumps({
#            "number" : number
#        }))
        return Response(number)
    
        
    @action(detail=False)
    def cabinets_by_name(self, request):
        cabs = Cabinet.objects.all().values_list('cab_name', flat=True)
#        cabsdata = {'cabs' : list(cabs)}
#        print(cabsdata)
#        jsoncabs = json.dumps(cabsdata)
#        print(jsoncabs)
        return Response(json.dumps({
            "cabs" : list(cabs)
        }))

    
    @action(detail=False, methods=['post'])
    def my_cabinets(self, request):
        print(request.data['number'])
        guest_key = request.data['number']
        guest = Guest.objects.all().filter(number=guest_key)[0]
        cabinets = [int(x) for x in guest.cabinets.split()]
        cabs = Cabinet.objects.all().filter(cab_number__in=cabinets)
        cabs_list = [x for x in cabs.values_list('cab_name', flat=True)]
        print(str(guest.cabinet))
        return Response(json.dumps({
            "cabs" : cabs_list,
            "current_cab" : str(guest.cabinet)
        }))

    
    @action(detail=False, methods=['post'])
    def check_cabinet_key(self, request):
        cabs = list(Cabinet.objects.all().values_list('key', flat=True))
        if int(request.POST['json_s']) in cabs:
#            answer = 'True'
#            jsonans = json.dumps(answer)
            return Response(json.dumps({
                "cabs" : True
            }))
        else:
#            answer = {'cabs' : 'False'}
#            jsonans = json.dumps(answer)
            return Response(json.dumps({
                "cabs" : False
            }))

        
    @action(detail=False, methods=['post'])
    def check_guest_key(self, request):
        keys = Guest.objects.values_list('number', flat=True)
        if int(request.POST['json_s']) in keys:
#            answer = 'True'
#            jsonans = json.dumps(answer)
            return Response(json.dumps({
                "guest" : True
            }))
        else:
#            answer = {'guest' : 'False'}
#            jsonans = json.dumps(answer)
            return Response(json.dumps({
                "guest" : False
            }))
        
    @action(detail=False, methods=['post'])
    def count_people(self, request):
        guest_key = int(json.loads(request.POST['json_s']))
        guest = Guest.objects.all().filter(number=guest_key)[0]
        guests = Guest.objects.all().filter(cabinet=guest.cabinet).order_by('number')
        k = 0
        for g in guests:
            if g == guest:
                answer = k
                jsonans = json.dumps(answer)
                return Response(jsonans)
            k += 1
        answer = k
        jsonans = json.dumps(answer)
        return Response(json.dumps({
            "count" : answer
        }))
    
    
    @action(detail=False, methods=['post'])
    def query_to_cabinet(self, request):
        cab_key = int(request.POST['json_s'])
        cab = Cabinet.objects.all().filter(key=cab_key)[0]
        guests1 = Guest.objects().all().filter(cabinet=cab)
        guests2 = [x for x in Guest.objects().all() if cab.cab_number in [int(t) for t in x.cabintes.split()]]
        return Response(json.dumps({
            "now" : len(guests1),
            "all" : len(guests2)
        }))
    
        
    @action(detail=False, methods=['post'])
    def next_guest(self, request):
        cab_key = int(request.POST['json_s'])
        cab = list(Cabinet.objects.all().filter(key=cab_key))[0]
        if len(list(Cabinet.objects.all().filter(key=cab_key))) == 0:
#            answer = 'False'
#            jsonans = json.dumps(answer)
            return Response(json.dumps({
                "status" : False
            }))
        guests = Guest.objects.all().filter(cabinet=cab).order_by('number')
        if len(guests) == 0:
#            answer = 'False'
#            jsonans = json.dumps(answer)
            return Response(json.dumps({
                "status" : False
            }))
        guest1 = int(str(guests[0]))
        guest2 = -1
        if len(guests) > 1:
            guest2 = int(str(guests[1]))
        que = [int(x) for x in guests[0].cabinets.split()]
        que.sort()
        que.remove(cab.cab_number)
        Guest.objects.filter(number=guests[0].number).update(cabinets=' '.join([str(x) for x in que]))
        cabs = Cabinet.objects.all().filter(cab_number__in=que)
        cabs_list = ' '.join([str(x) for x in cabs.values_list('cab_number', flat=True)])
        if len(cabs) > 0:
            min_cab = cabs[0]
            min_len = len(Guest.objects.all().filter(cabinet=min_cab))
            for c in cabs:
                if len(Guest.objects.all().filter(cabinet=c)) < min_len:
                    min_len = len(Guest.objects.all().filter(cabinet=c))
                    min_cab = c
            
            Guest.objects.filter(number=guests[0].number).update(cabinet=min_cab)
        else:
            Guest.objects.filter(number=guests[0].number).delete()
#        answer = 'True'
#        jsonans = json.dumps(answer)
        MovedGuest.objects.create(guest_key=guest1)
        if guest2 != -1:
            MovedGuest.objects.create(guest_key=guest2)
        return Response(json.dumps({
            "status" : True,
            "guest1" : guest1,
            "guest2" : guest2
        }))
    
    
    @action(detail=False)
    def get_schedule(self, request):
        names = list()
        query = list()
        max_len = 0
        for cab in Cabinet.objects.all():
            names.append(cab.cab_name)
            query.append([])
            for g in Guest.objects.all().filter(cabinet=cab).order_by('number'):
                query[len(query) - 1].append(str(g.number))
            if max_len < len(query[len(query) - 1]):
                max_len = len(query[len(query) - 1])
        for q in query:
            while len(q) < max_len:
                q.append('-')
        queryform = list()
        for i in range(0, len(query[0])):
            queryform.append([])
            for j in range(0, len(query)):
                queryform[i].append(query[j][i])
        print(queryform)
#        answer = {'names' : names,
#                  'guests' : queryform}
        return Response(json.dumps({
            "names" : names,
            "guests" : queryform
        }))

    
    @action(detail=False, methods=['get'])
    def get_moved_guests(self, request):
        guests_to_notify = [int(str(x)) for x in MovedGuest.objects.all()]
        if len(guests_to_notify) == 0:
            return Response(json.dumps({
                "empty" : True,
                "guests" : guests_to_notify
            }))
        MovedGuest.objects.all().delete()
        return Response(json.dumps({
            "empty" : False,
            "guests" : guests_to_notify
        }))