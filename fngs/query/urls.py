from django.conf.urls import url
from . import views


app_name = 'query'

urlpatterns = [
	url(r'^$', views.query_job, name='index'),
	url(r'job/submit/$', views.query_job, name='query-job'),
]
