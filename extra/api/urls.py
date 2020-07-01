from django.urls import path
from .views import *
app_name='extra'
urlpatterns=[
    path('terms_and_condition/',TermsAndCondition.as_view(),name='terms_and_condition'),
    path('about_us/',AboutUs.as_view(),name='about_us'),
    path('legal/',Legal.as_view(),name='legal'),
]
