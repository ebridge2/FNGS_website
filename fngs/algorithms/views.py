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
import csv

def index(request):
	return render(request, 'algorithms/index.html')

def submit_job(request):
	form = SubmissionForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		submission = form.save(commit=False)
		submission.creds_file = request.FILES['creds_file']
		if submission.upload_data_or_not == "Yes":
			submission.data_file = request.FILES['data_file']
		submission.save()
		logfile = submission.jobdir + "log.txt"
		p1 = Process(target=unzipstuff, args=(submission,))
		p1.daemon=True
		p1.start()
		p1.join()
		p2 = Process(target=uploadstuff, args=(submission,))
		p2.daemon=True
		p2.start()
		p2.join()
		p3 = Process(target=deletestuff, args=(submission,))
		p3.daemon=True
		p3.start()
		p3.join()
		p4 = Process(target=submitstuff, args=(submission, logfile))
		p4.daemon=True
		p4.start()
		p4.join()
		messages = open(logfile, 'r').readlines()
		os.system("rm " + logfile)
		context = {
			"messages": messages,
			"form": form,
		}
		return render(request, 'algorithms/create_submission.html', context)
	form.fields['state'].widget.attrs['readonly'] = True
	form.fields['bucket'].widget.attrs['readonly'] = True
	form.fields['bidsdir'].widget.attrs['readonly'] = True
	form.fields['datasetname'].widget.attrs['readonly'] = True
	form.fields['modality'].widget.attrs['readonly'] = True
	form.fields['slice_timing'].widget.attrs['readonly'] = True
	form.fields['upload_data_or_not'].widget.attrs['readonly'] = True
	context = {
		"form": form,
	}
	return render(request, 'algorithms/create_submission.html', context)

def unzipstuff(submission):
	if submission.upload_data_or_not == "Yes":
		filename = submission.data_file.name[:-4]
		cmd = "mkdir " + filename
		os.system(cmd)
		cmd = "unzip " + submission.data_file.url + " -d " + filename
		os.system(cmd)
		
def uploadstuff(submission):
	if submission.upload_data_or_not == "Yes":
		creds = submission.creds_file.url
    		credfile = open(creds, 'rb')
    		reader = csv.reader(credfile)
    		rowcounter = 0
    		for row in reader:
        		if rowcounter == 1:
            			public_access_key = str(row[0])
            			secret_access_key = str(row[1])
        		rowcounter = rowcounter + 1
		os.environ['AWS_ACCESS_KEY_ID'] = public_access_key
    		os.environ['AWS_SECRET_ACCESS_KEY'] = secret_access_key
    		os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
		cmd = "aws s3 sync " + submission.data_file.name[:-4] + " s3://" + submission.bucket + " --acl public-read"
		os.system(cmd)
		
def deletestuff(submission):
	if submission.upload_data_or_not == "Yes":
		cmd = "rm -rf " + submission.data_file.name[:-4] + "/"
		os.system(cmd)
		submission.data_file.delete()

def submitstuff(submission, logfile):
	if submission.state == 'Participant analysis':
		cmd = "ndmg_cloud participant --bucket " + submission.bucket + " --bidsdir " + submission.bidsdir + " --jobdir " + submission.jobdir + " --credentials " + submission.creds_file.url + " --modality func --stc interleaved"
	if submission.state == 'group':
		cmd = "ndmg_cloud group --bucket " + submission.bucket + " --bidsdir " + submission.bidsdir + " --jobdir " + submission.jobdir + " --credentials " + submission.creds_file.url + " --modality " + submission.modality + " --dataset " + submission.datasetname
	cmd = cmd + " > " + logfile
	os.system(cmd)
