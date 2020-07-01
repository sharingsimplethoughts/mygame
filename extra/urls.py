from django.urls import path
from .views import *

app_name="extra_web"

urlpatterns=[
    path('terms_and_condition/',TermsAndConditionView.as_view(),name='terms_and_condition_webview'),
    path('about_us/',AboutUsView.as_view(),name='about_us_webview'),
    path('legal/',LegalView.as_view(),name='legal_webview'),
    path('privacypolicy/',PrivacyPolicyView.as_view(),name='privacypolicy'),
]
