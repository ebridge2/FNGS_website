from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Submission
from .forms import SubmissionForm
from ndmg.scripts.ndmg_func_pipeline import ndmg_func_pipeline as fngs_pipeline
from ndmg.scripts.ndmg_dwi_pipeline import ndmg_dwi_pipeline as ndmg_pipeline
from django.conf import settings
import time
import importlib
import imp
from ndmg.utils import utils as mgu
from threading import Thread
from multiprocessing import Process
import os
import re

def index(request):
	return render(request, 'analyze/index.html')

def submit_job(request):
	form = SubmissionForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		submission = form.save(commit=False)
		submission.creds_file = request.FILES['creds_file']
		submission.data_file = request.FILES['data_file']
		submission.save()
		logfile = submission.jobdir + "log.txt"
		p1 = Process(target=unzipstuff, args=(submission))
		p1.daemon=True
		p1.start()
		p1.join()
		p2 = Process(target=submitstuff, args=(submission, logfile))
		p2.daemon=True
		p2.start()
		p2.join()
		messages = open(logfile, 'r').readlines()
		os.system("rm " + logfile)
		context = {
			"messages": messages,
			"form": form,
		}
		return render(request, 'analyze/create_submission.html', context)
	context = {
		"form": form,
	}
	return render(request, 'analyze/create_submission.html', context)

def unzipstuff(submission):
	if submission.data_file is not "":
		filename = submission.data_file[:-4]
		cmd = "mkdir " + filename
		os.system(cmd)
		cmd = "unzip " + submission.data_file + " -d " + filename
		os.system(cmd)

def submitstuff(submission, logfile):
	if submission.state == 'participant':
		cmd = "ndmg_cloud participant --bucket " + submission.bucket + " --bidsdir " + submission.bidsdir + " --jobdir " + submission.jobdir + " --credentials " + submission.creds_file.url + " --modality " + submission.modality + " --stc " + submission.slice_timing
	if submission.state == 'group':
		cmd = "ndmg_cloud group --bucket " + submission.bucket + " --bidsdir " + submission.bidsdir + " --jobdir " + submission.jobdir + " --credentials " + submission.creds_file.url + " --modality " + submission.modality + " --dataset " + submission.datasetname
	cmd = cmd + " > " + logfile
	os.system(cmd)
