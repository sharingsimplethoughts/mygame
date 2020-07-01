from django.db import models
#..
class TemporaryStorage(models.Model):
    room_name=models.CharField(max_length=500,default='')
    room_pass=models.CharField(max_length=100,default='12345678')

    def __str__(self):
        return self.room_name