from django.urls import path

from enrollment.messaging import views

app_name = 'messaging'
urlpatterns = [
    path('sms', views.sms_response, name='sms'),
    path('sms/status', views.sms_status, name='sms-status'),
]
