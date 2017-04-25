from django.conf.urls import url
from . import views


app_name = 'analyze'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<dataset_id>[\w\-]+)/$', views.dataset, name='dataset'),
	url(r'dataset/add/$', views.create_dataset, name='dataset-add'),
	url(r'job/submit/$', views.submit_job, name='job-submit'),
	url(r'dataset/(?P<dataset_id>[\w\-]+)/delete/$', views.delete_dataset, name='dataset-delete'),
	url(r'dataset/(?P<dataset_id>[\w\-]+)/subject/add/$', views.create_subject, name='subject-add'),
	url(r'dataset/(?P<dataset_id>[\w\-]+)/(?P<sub_id>[\w\-]+)/delete/$', views.delete_subject, name='subject-delete'),
	url(r'dataset/(?P<dataset_id>[\w\-]+)/(?P<sub_id>[\w\-]+)/analyze/$', views.analyze_subject, name='subject-analyze'),
	url(r'dataset/(?P<dataset_id>[\w\-]+)/(?P<sub_id>[\w\-]+)/results/$', views.get_results, name='subject-results'),
]
