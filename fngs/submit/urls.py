from django.conf.urls import url
from . import views


app_name = 'submit'

urlpatterns = [
	url(r'^$', views.submit_job, name='index'),
	url(r'demo/$', views.demo_job, name='demo'),
	url(r'job/submit/$', views.submit_job, name='job-submit'),
]
