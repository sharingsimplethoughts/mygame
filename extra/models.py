from django.db import models

# Create your models here.
class AboutUs(models.Model):
    title=models.CharField(max_length=100,default='')
    content=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'About Us-'+str(self.id)

class TermsAndCondition(models.Model):
    title=models.CharField(max_length=100,default='')
    content=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Terms and Condition-'+str(self.id)

class Legal(models.Model):
    title=models.CharField(max_length=100,default='')
    content=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Legal-'+str(self.id)

class PrivacyPolicy(models.Model):
    title=models.CharField(max_length=100,default='')
    content=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Privacy Policy-'+str(self.id)
