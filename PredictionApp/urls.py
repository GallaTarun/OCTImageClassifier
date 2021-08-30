from django.conf.urls import include,url
from PredictionApp import views

app_name = 'prediction_app'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^predict/$',views.predict,name='predict'),
    url(r'^about_us/$',views.about_us, name='about_us'),
    url(r'^architecture',views.architecture, name='architecture')
]

