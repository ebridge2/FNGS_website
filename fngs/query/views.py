from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import QuerySubmission
from .forms import QuerySubmissionForm
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
	return render(request, 'query/index.html')

def query_job(request):
	form = QuerySubmissionForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		submission = form.save(commit=False)
		submission.creds_file = request.FILES['creds_file']
		submission.save()
		logfile = submission.jobdir + "log.txt"
		p = Process(target=submit_query, args=(submission, logfile))
		p.daemon=True
		p.start()
		p.join()
		messages = open(logfile, 'r').readlines()
		os.system("rm " + logfile)
		if submission.state == 'kill':
			counter = 0
			new_messages = []
			for i in range(len(messages)):
				if (messages[i][0:7] == "... Can") or (messages[i][0:7] == "... Ter"):
					counter = counter + 1
					new_messages.append(messages[i])
			new_messages.append("Killed " + str(counter) + " jobs successfully!")
			messages = new_messages
		context = {
			"messages": messages,
			"form": form,
		}
		return render(request, 'query/new_query.html', context)
	context = {
		"form": form,
	}
	return render(request, 'query/new_query.html', context)

def submit_query(query, logfile):
	cmd = "ndmg_cloud {} --jobdir {} --credentials {}".format(query.state,
		query.jobdir, query.creds_file.url)
	os.system(cmd)
