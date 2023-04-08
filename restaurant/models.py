from django.db import models
from manager.models import Station

# Create your models here.
class Restaurant(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    mobile = models.CharField(max_length=10)
    name = models.CharField(max_length=40)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name + ' , ' + self.station.name

class FoodItem(models.Model):
    name = models.CharField(max_length=40)
    price = models.IntegerField()
    f_time = models.IntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' , ' + self.restaurant.name