from django.db import models


class Cabinet(models.Model):
    cab_number = models.BigIntegerField(unique=True)
    cab_name = models.CharField(max_length=255, unique=True)
    tg_id = models.BigIntegerField(blank=True)
    key = models.BigIntegerField()
    query = models.TextField(blank=True)
    
    def __str__(self):
        return self.cab_name
    

class Guest(models.Model):
    number = models.IntegerField(unique=True)
    tg_id = models.BigIntegerField(default=-1)
    cabinets = models.TextField()
    cabinet = models.ForeignKey(Cabinet, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return str(self.number)
    
    
class MovedGuest(models.Model):
    guest_key = models.IntegerField()
    
    def __str__(self):
        return str(self.guest_key)
    
'''    
class Schedule(models.Model):
    query = models.CharField()
    
    
    def __str__(self):
        return 'Query'
'''