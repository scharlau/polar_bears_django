from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.

class Bear(models.Model):
    bearID = models.IntegerField()
    pTT_ID = models.IntegerField()
    capture_lat = models.FloatField()
    capture_long = models.FloatField()
    sex = models.TextField()
    age_class = models.TextField()
    ear_applied = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        app_label = 'bears'

    def __str__(self):
        return self.bearID+" "+self.pTT_ID+" "+self.capture_lat+" "+self.capture_long+" "+self.sex+" "+self.age_class+" "+self.ear_applied+" "+self.created_date

    
