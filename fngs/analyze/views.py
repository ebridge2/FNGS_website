from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Dataset, Subject
from .forms import DatasetForm, SubjectForm
from ndmg.scripts.fngs_pipeline import fngs_pipeline
from ndmg.scripts.ndmg_pipeline import ndmg_pipeline
from django.conf import settings
import time
import importlib
import imp
from ndmg.utils import utils as mgu
from threading import Thread
from multiprocessing import Process
import os
import re


BRAIN_FILE_TYPES = ['nii', 'nii.gz']

def index(request):
	datasets = Dataset.objects.all()
	return render(request, 'analyze/index.html', {'datasets': datasets})


def dataset(request, dataset_id):
	dataset = get_object_or_404(Dataset, dataset_id=dataset_id)
	return render(request, 'analyze/dataset.html', {'dataset': dataset})

def create_dataset(request):
	form = DatasetForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		for dataset in Dataset.objects.all():
			if dataset.dataset_id == form.cleaned_data.get("dataset_id"):
				context = {
					'dataset': dataset,
					'error_message': 'You already added that dataset.',
				}
				return render(request, 'analyze/create_dataset.html', context)
		dataset = form.save(commit=False)
		dataset.output_url = str(settings.OUTPUT_DIR + dataset.dataset_id)
		mgu().execute_cmd("mkdir -p " + str(dataset.output_url))
		dataset.save()
		return render(request, 'analyze/dataset.html', {'dataset': dataset})
	context = {
		"form": form,
	}
	return render(request, 'analyze/create_dataset.html', context)

def create_subject(request, dataset_id):
	form = SubjectForm(request.POST or None, request.FILES or None)
	dataset = get_object_or_404(Dataset, dataset_id=dataset_id)
	if form.is_valid():
		dataset_subs = dataset.subject_set.all()
		for sub in dataset_subs:
			if sub.sub_id == form.cleaned_data.get("sub_id"):
				context = {
					'dataset': dataset,
					'form': form,
					'error_message': 'You already added that subject',
				}
				return render(request, 'analyze/create_subject.html', context)
		subject = form.save(commit=False)
		subject.dataset = dataset
		subject.struct_scan = request.FILES['struct_scan']
		file_type = subject.struct_scan.url.split('.', 1)[-1]
		file_type = file_type.lower()
		if file_type not in BRAIN_FILE_TYPES:
			context = {
				'album': dataset,
				'form': form,
				'error_message': 'Brain File must be .nii or .nii.gz',
			}
			return render(request, 'analyze/create_subject.html', context)
		subject.func_scan = request.FILES['func_scan']
		file_type = subject.func_scan.url.split('.', 1)[-1]
		file_type = file_type.lower()
		if file_type not in BRAIN_FILE_TYPES:
			context = {
				'dataset': dataset,
				'form': form,
				'error_message': 'Brain File must be .nii or .nii.gz',
			}
			return render(request, 'analyze/create_subject.html', context)             
		subject.dti_file = request.FILES['dti_file']
		subject.bvals_file = request.FILES['bvals_file']
		subject.bvecs_file = request.FILES['bvecs_file']
		subject.save()
		return render(request, 'analyze/dataset.html', {'dataset': dataset})
	context = {
		"form": form,
	}
	return render(request, 'analyze/create_subject.html', context)

def analysis(dataset_id, dataset, sub_id, output_dir):
	subject = get_object_or_404(Subject, dataset=dataset, sub_id=sub_id)
	subject.output_url = output_dir

	ndmg_outdir = settings.OUTPUT_DIR + dataset_id + "/ndmgresults"
	#ndmg_pipeline(subject.dti_file.url, subject.bvals_file.url, subject.bvecs_file.url, subject.mprage_file.url, settings.AT_FOLDER + '/atlas/MNI152_T1_2mm.nii.gz', settings.AT_FOLDER + '/mask/MNI152_T1_2mm_brain_mask.nii.gz', [settings.AT_FOLDER + '/label/desikan_2mm.nii.gz'], ndmg_outdir)

	ndmg_run_cmd = "ndmg_pipeline " + str(subject.dti_file.url) + " " + str(subject.bvals_file.url) + " " + str(subject.bvecs_file.url) +\
		" " + str(subject.struct_scan.url) + " " + str(settings.AT_FOLDER + '/atlas/MNI152_T1-2mm.nii.gz') + " " + str(settings.AT_FOLDER +\
		'/mask/MNI152_T1-2mm_brain_mask.nii.gz') + " " + ndmg_outdir + " " + settings.AT_FOLDER + '/label/desikan-2mm.nii.gz'
	mgu().execute_cmd(ndmg_run_cmd)

	ndmg_bids = imp.load_source('ndmg_bids', '/ndmg/ndmg/scripts/ndmg_bids')
	ndmg_bids.group_level(ndmg_outdir+"/graphs/", ndmg_outdir+"/qc", False)
c
	#ndmg_bids_cmd = "ndmg_bids " + ndmg_outdir + "/graphs/ " + ndmg_outdir + "/qc group"
	#mgu().execute_cmd(ndmg_bids_cmd)

	fngs_pipeline(subject.func_scan.url, subject.struct_scan.url, subject.an,
				   settings.AT_FOLDER + '/atlas/MNI152_T1-2mm.nii.gz', settings.AT_FOLDER + '/atlas/MNI152_T1-2mm_brain.nii.gz',
				   settings.AT_FOLDER + '/mask/MNI152_T1-2mm_brain_mask.nii.gz', settings.AT_FOLDER + '/mask/HarvOx_lv_thr25-2mm.nii.gz', 
				   [settings.AT_FOLDER + '/label/desikan-2mm.nii.gz'], output_dir, stc=subject.slice_timing, fmt='graphml')



	wd = os.getcwd()
	# go to where the subject is
	os.chdir(dataset.output_url)
	sub_folder = re.split('/', subject.output_url)[-1]

	mgu().execute_cmd('zip -r ' + str(sub_folder) + ".zip *")
	# change directory back
	os.chdir(wd)
	# and update the subject
	subject.save() # updated the output location, so save the updated subject

def analyze_subject(request, dataset_id, sub_id):
	dataset = get_object_or_404(Dataset, dataset_id=dataset_id)
	subject = get_object_or_404(Subject, dataset=dataset, sub_id=sub_id)
	try:
		# update subject save location
		if subject.output_url is not None:
			mgu().execute_cmd("rm -rf " + subject.output_url)
		subject.output_url = None
		subject.save()
		date = time.strftime("%d-%m-%Y")
		output_dir = settings.OUTPUT_DIR + dataset_id + "/" + sub_id + "_" + date
		p = Process(target=analysis, args=(dataset_id, dataset, sub_id, output_dir,))
		p.daemon=True
		p.start()
	except:
		raise Http404
	return render(request, 'analyze/dataset.html', {'dataset':dataset})

def get_results(request, dataset_id, sub_id):
	pass

def delete_dataset(request, dataset_id):
	dataset = get_object_or_404(Dataset, dataset_id=dataset_id)
	# get the subjects of this dataset to delete all of them
	try:
		subjects = Subject.objects.get(dataset=dataset)
	except Subject.DoesNotExist:
		subjects=None
	if subjects:
		return HttpResponse("There are subjects in here!", status=404)
	else:
		dataset.delete()
		datasets = Dataset.objects.all()
		return render(request, 'analyze/index.html', {'datasets': datasets})


def delete_subject(request, dataset_id, sub_id):
	dataset = get_object_or_404(Dataset, dataset_id=dataset_id)
	subject = get_object_or_404(Subject, dataset=dataset, sub_id=sub_id)
	# clear all traces of the subject from our storage system
	mgu().execute_cmd("rm -rf " + subject.func_scan.url)
	mgu().execute_cmd("rm -rf " + subject.struct_scan.url)
	mgu().execute_cmd("rm -rf " + subject.dti_file.url)
	mgu().execute_cmd("rm -rf " + subject.bvals_file.url)
	mgu().execute_cmd("rm -rf " + subject.bvecs_file.url)
	if subject.output_url is not None:
		mgu().execute_cmd("rm -rf " + subject.output_url)
	subject.delete()
	datasets = Dataset.objects.all()
	return render(request, 'analyze/dataset.html', {'dataset': dataset})
