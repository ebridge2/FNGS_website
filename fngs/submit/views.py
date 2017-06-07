from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Submission
from .forms import SubmissionForm
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
import itertools
from collections import OrderedDict
from shutil import rmtree

def index(request):
    return render(request, 'submit/index.html')

def upload_submit(target_funcs, args, logfile):
    for (target, arg) in zip(target_funcs, args):
        proc = Process(target=target, args=arg)
        proc.daemon = True
        proc.start()
        proc.join()
    messages = open(logfile, 'r').readlines()
    os.remove(logfile)
    new_messages = []
    counter = 0
    for i in range(len(messages)):
        if messages[i][0:18] == "... Submitting job":
            counter += 1
            new_messages.append(messages[i])
            if i == (len(messages) - 1):
                counter = 0
                new_messages = []
    new_messages.append("Submitted " + str(counter) + " jobs successfully!")
    return new_messages

def submit_job(request):
    form = SubmissionForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        submission = form.save(commit=False)
        submission.creds_file = request.FILES['creds_file']
        if submission.upload_data_or_not == "yes":
            submission.data_file = request.FILES['data_file']
        submission.save()
        logfile = submission.jobdir + "log.txt"
        target_funcs = [unzip_directory, upload_bids, cleanup, submit]
        args = [(submission,), (submission,), (submission,), (submission, logfile)]
        new_messages = upload_submit(target_funcs, args, logfile)
        context = {
            "messages": new_messages,
            "form": form,
        }
        return render(request, 'submit/create_submission.html', context)
    context = {
        "form": form,
    }
    return render(request, 'submit/create_submission.html', context)

def unzip_directory(submission):
    if submission.upload_data_or_not == "yes":
        filename = submission.data_file.name[:-4]
        cmd = "mkdir " + filename
        os.system(cmd)
        cmd = "unzip " + submission.data_file.url + " -d " + filename
        os.system(cmd)
    pass

def upload_bids(submission):
    if submission.upload_data_or_not == "yes":
        print(submission.creds_file.url)
        credfile = open(submission.creds_file.url, 'rb')
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
    pass

def cleanup(submission):
    if submission.upload_data_or_not == "yes":
        rmtree(submission.data_file.name[:-4])
        submission.data_file.delete()
    pass

def submit(submission, logfile):
    cmd = ("ndmg_cloud {} --bucket {} --bidsdir {} --jobdir {} --credentials {}"
           " --modality {} --stc {} > {}").format(submission.state, submission.bucket,
                submission.bidsdir, submission.jobdir, submission.creds_file.url, 
                submission.modality, submission.slice_timing, logfile)
    print(cmd)
    os.system(cmd)

def demo_job(request):
    form = SubmissionForm(request.POST or None, request.FILES or None)
    fields = ['bucket', 'bidsdir', 'datasetname', 'upload_data_or_not']
    defaults = ['fngs-test', 'BNU1-demo', 'BNU1', 'yes']
    disable = ['state', 'data_file', 'slice_timing']
    for (field, default) in zip(fields, defaults):
        form.initial[field] = default
    for field in itertools.chain(fields, disable):
        form.fields[field].disabled = True
    if form.is_valid():
        submission = form.save(commit=False)
        submission.creds_file = request.FILES['creds_file']
        submission.save()
        logfile = submission.jobdir + "log.txt"
        target_funcs = [unzip_directory, upload_demo, submit]
        args = [(submission,), (submission,), (submission, logfile)]
        new_messages = upload_submit(target_funcs, args, logfile)
        context = {
            "messages": new_messages,
            "form": form,
        }
        return render(request, 'submit/create_submission.html', context)
    context = {
        "form": form,
    }
    return render(request, 'submit/create_submission.html', context)

def upload_demo(submission):
    credfile = open(submission.creds_file.url, 'rb')
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
    demo_dir = '/FNGS_server/demo_data/BNU1-demo'
    cmd = "aws s3 sync " + demo_dir + " s3://" + submission.bucket + " --acl public-read"
    os.system(cmd)