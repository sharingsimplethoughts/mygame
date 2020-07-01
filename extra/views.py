from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
# Create your views here.
class TermsAndConditionView(TemplateView):
    def get(self,request,*args,**kwargs):
        tacond=TermsAndCondition.objects.all().first()
        return render(request,'extra/terms-conditions.html',{'tacond':tacond})

class AboutUsView(TemplateView):
    def get(self,request,*args,**kwargs):
        aboutus=AboutUs.objects.all().first()
        return render(request,'extra/about-us.html',{'aboutus':aboutus})

class LegalView(TemplateView):
    def get(self,request,*args,**kwargs):
        legal=Legal.objects.all().first()
        return render(request,'extra/legal.html',{'legal':legal})

class PrivacyPolicyView(TemplateView):
    def get(self,request,*args,**kwargs):
        privacypolicy=PrivacyPolicy.objects.all().first()
        return render(request,'extra/privacy-policy.html',{'privacypolicy':privacypolicy})
