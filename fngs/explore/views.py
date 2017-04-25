from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic
from analyze.models import Dataset, Subject
import os
from ndmg.utils import utils as mgu
import nibabel as nb

def index(request):
	datasets = Dataset.objects.all()
	return render(request, 'explore/index.html', {'datasets': datasets})

def dataset(request, dataset_id):
	dataset = get_object_or_404(Dataset, dataset_id=dataset_id)
	return render(request, 'explore/dataset.html', {'dataset': dataset})

def download_subject(request, dataset_id, sub_id):
	dataset = get_object_or_404(Dataset, dataset_id=dataset_id)
	subject = get_object_or_404(Subject, dataset = dataset, sub_id = sub_id)
	## TODO: handle this better here; don't just return the same page
	if subject.output_url is not None:
		file_path = subject.output_url + ".zip"
		if os.path.exists(file_path):
			with open(file_path, 'rb') as fh:
				response = HttpResponse(fh.read(), content_type='application/zip')
				response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
				return response
		else:
			raise Http404
	return render(request, 'explore/dataset.html', {'dataset': dataset})

def sub_overall_qc(request, dataset_id, sub_id):
	dataset = get_object_or_404(Dataset, dataset_id=dataset_id)
	subject = get_object_or_404(Subject, dataset = dataset, sub_id = sub_id)
	if subject.output_url is not None:
		scan = nb.load(subject.func_scan.url)
		res = scan.header.get_zooms()
		context = {'dataset': dataset,
				   'subject': subject,
				   'res': res[0:3],
				   'tr': res[3]
		}
		return render(request, 'explore/overall.html', context)
	else:
		raise Http404("Either the subject is currently being analyzed, or you have not analyzed this subject yet.")

def sub_motion_qc(request, dataset_id, sub_id):
	dataset = get_object_or_404(Dataset, dataset_id=dataset_id)
	subject = get_object_or_404(Subject, dataset = dataset, sub_id = sub_id)
	test = mgu.execute_cmd("find " + subject.output_url + " -wholename \"*overall*" + subject.get_id() + "*trans*\"")[0].rstrip('\n')
	context = {'dataset': dataset,
			   'subject': subject,
			   'trans': mgu.execute_cmd("find " + subject.output_url + " -wholename \"*overall*" + subject.get_id() + "*trans*\"")[0].rstrip('\n'),
			   'rot': mgu.execute_cmd("find " + subject.output_url + " -wholename \"*overall*" + subject.get_id() + "*rot*\"")[0].rstrip('\n'),
			   'disp': mgu.execute_cmd("find " + subject.output_url + " -wholename \"*overall*" + subject.get_id() + "*disp*\"")[0].rstrip('\n'),
			   'mcjitter':mgu.execute_cmd("find " + subject.output_url + " -wholename \"*mc*" + subject.get_id() + "*jitter*\"")[0].rstrip('\n'),
			   'mckde':mgu.execute_cmd("find " + subject.output_url + " -wholename \"*mc*" + subject.get_id() + "*kde*\"")[0].rstrip('\n')}
	return render(request, 'explore/motion.html', context)

def sub_stats_qc(request, dataset_id, sub_id):
	dataset = get_object_or_404(Dataset, dataset_id=dataset_id)
	subject = get_object_or_404(Subject, dataset = dataset, sub_id = sub_id)
	context = {'dataset': dataset,
			   'subject': subject,
			   'std': mgu.execute_cmd("find " + subject.output_url + " -wholename \"*overall*" + subject.get_id() + "*std*\"")[0].rstrip('\n'),
			   'snr': mgu.execute_cmd("find " + subject.output_url + " -wholename \"*overall*" + subject.get_id() + "*snr*\"")[0].rstrip('\n'),
			   'intens': mgu.execute_cmd("find " + subject.output_url + " -wholename \"*overall*" + subject.get_id() + "*intens*\"")[0].rstrip('\n'),
			   'voxel_hist': mgu.execute_cmd("find " + subject.output_url + " -wholename \"*overall*" + subject.get_id() + "*hist*\"")[0].rstrip('\n')}
	return render(request, 'explore/stats.html', context)

def sub_register_qc(request, dataset_id, sub_id):
	dataset = get_object_or_404(Dataset, dataset_id=dataset_id)
	subject = get_object_or_404(Subject, dataset = dataset, sub_id = sub_id)
	context = {'dataset': dataset,
			   'subject': subject,
			   'mean_anat': mgu.execute_cmd("find " + subject.output_url + " -wholename \"*overall*" + subject.get_id() + "*mean_anat*\"")[0].rstrip('\n'),
			   'mean_ref': mgu.execute_cmd("find " + subject.output_url + " -wholename \"*overall*" + subject.get_id() + "*mean_ref*\"")[0].rstrip('\n'),
			   'anat_ref': mgu.execute_cmd("find " + subject.output_url + " -wholename \"*overall*" + subject.get_id() + "*anat_ref*\"")[0].rstrip('\n'),
			   'reg_jitter': mgu.execute_cmd("find " + subject.output_url + " -wholename \"*reg*" + subject.get_id() + "*jitter*\"")[0].rstrip('\n'),
			   'reg_kde': mgu.execute_cmd("find " + subject.output_url + " -wholename \"*reg*" + subject.get_id() + "*kde*\"")[0].rstrip('\n')}
	return render(request, 'explore/register.html', context)
	
def sub_nuisance_qc(request, dataset_id, sub_id):
	dataset = get_object_or_404(Dataset, dataset_id=dataset_id)
	subject = get_object_or_404(Subject, dataset = dataset, sub_id = sub_id)
	context = {
			   'dataset':dataset,
			   'subject':subject,
			   'var': mgu.execute_cmd("find " + subject.output_url + " -wholename \"*nuis*" + subject.get_id() + "*scree*\"")[0].rstrip('\n'),
			   'er2ma': mgu.execute_cmd("find " + subject.output_url + " -wholename \"*eroded_wm*" + subject.get_id() + "*wm_overlap*\"")[0].rstrip('\n'),
			   'ma2br': mgu.execute_cmd("find " + subject.output_url + " -wholename \"*eroded_wm*" + subject.get_id() + "*aligned_overlap*\"")[0].rstrip('\n'),
	}
	return render(request, 'explore/nuisance.html', context)

def sub_timeseries_qc(request, dataset_id, sub_id):
	dataset = get_object_or_404(Dataset, dataset_id=dataset_id)
	subject = get_object_or_404(Subject, dataset = dataset, sub_id = sub_id)
	labels = os.listdir(subject.output_url + "/roi_timeseries/")
	labelled_atlas = {}
	for label in labels:
		at2label = mgu.execute_cmd("find " + subject.output_url + " -wholename \"*roi*" + "MNI" + "*" + label + "*overlap*\"")[0].rstrip('\n')
		timeseries = mgu.execute_cmd("find " + subject.output_url + " -wholename \"*roi*" + subject.get_id() + "*" + label + "*timeseries*\"")[0].rstrip('\n')
		corr = mgu.execute_cmd("find " + subject.output_url + " -wholename \"*roi*" + subject.get_id() + "*" + label + "*cor*\"")[0].rstrip('\n')
		labelled_atlas[label] = Label_Atlas(at2label, timeseries, corr)
	context = {'dataset': dataset, 'subject': subject, 'labelled_atlas': labelled_atlas}
	return render(request, 'explore/timeseries.html', context)

class Label_Atlas:
	def __init__(self, at2label, timeseries, corr):
		self.at2label = at2label
		self.timeseries = timeseries
		self.corr = corr
		pass
