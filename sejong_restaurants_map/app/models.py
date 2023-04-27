from django.db import models

class restaurant(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=10)
    category=models.CharField(max_length=10)
    location_long=models.FloatField()
    location_lat=models.FloatField()

    class Meta:
        db_table='restaurant'