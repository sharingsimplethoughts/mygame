from django.db import models
from registration.models import *
# Create your models here.
class SubscriptionPlan(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    amount=models.PositiveIntegerField(default=0)
    validity=models.PositiveIntegerField(default=1)
    created_on=models.DateTimeField(auto_now=True)
    is_blocked=models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='subuser')
    plan=models.ForeignKey(SubscriptionPlan,on_delete=models.CASCADE,related_name='subplan')
    created_on=models.DateTimeField(auto_now=True)
    is_expired=models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.id)+'--'+self.plan.name+'--'+str(self.created_on)