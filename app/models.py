from django.db import models

class restaurant(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=10)
    category=models.CharField(max_length=10)
    location_long=models.FloatField()
    location_lat=models.FloatField()

    class Meta:
        db_table='restaurant'

#회원정보
class User(models.Model):
  email = models.CharField(max_length=20)
  name = models.CharField(max_length=20)
  pwd = models.CharField(max_length=20)

#게시판
class Article(models.Model):
  title = models.CharField(max_length=100)
  content = models.CharField(max_length=1000)
  user = models.ForeignKey(User, on_delete=models.CASCADE)