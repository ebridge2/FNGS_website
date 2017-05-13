from django.conf.urls import url
from . import views


app_name = 'explore'

urlpatterns = [
	url(r'^$', views.submit_job, name='index'),
	url(r'job/submit/$', views.submit_job, name='job-submit'),
]
