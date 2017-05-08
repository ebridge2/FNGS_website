from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
import os.path as op
import os
import uuid

def get_creds_file_path(instance, filename):
	return os.path.join("/".join(["creds", filename]))

def get_data_file_path(instance, filename):
	return os.path.join("/".join(["uploaded_data", filename]))

class Submission(models.Model):
	output_url = models.CharField(max_length=200, null=True, blank=True)
	STATE_CHOICES = (
		('participant', 'Participant analysis'),
		('group', 'Group analysis')
	)
	state = models.CharField(max_length=20, choices=STATE_CHOICES, default=None, blank=False)
	bucket = models.CharField(max_length=100, blank=False)
	bidsdir = models.CharField(max_length=100, blank=False)
	jobdir = models.CharField(max_length=100, blank=False)
	creds_file = models.FileField(upload_to=get_creds_file_path, null=True, blank=False)
	data_file = models.FileField(upload_to=get_data_file_path, null=True, blank=True)
	datasetname = models.CharField(max_length=100, blank=True)
	MOD_CHOICES = (
		('func', 'Functional'),
		("dwi", 'DWI')
	)
	modality = models.CharField(max_length=20, choices=MOD_CHOICES, default=None, blank=False)
	STC_CHOICES = (
		('None', 'None'),
		('up', 'Bottom Up Acquisition (standard)'),
		('down', 'Top Down Acquisition'),
		("interleaved", 'Interleaved Acquisition')
	)
	slice_timing = models.CharField(max_length=20, choices=STC_CHOICES, default=None, blank=False)
	UPLOAD_CHOICES = (
		('yes', 'Yes'),
		('no', 'No')
	)
	upload_data_or_not = models.CharField(max_length=20, choices=UPLOAD_CHOICES, default=None, blank=False)

	def add_output_url(self, url):
		output_url = models.TextField(url)
			
	def __str__(self):
		return str(self.bucket) + "/" + str(self.bidsdir)

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return (self.bucket == other.bucket) and (self.bidsdir == other.bidsdir)
		return False

	def __ne__(self, other):
		return not self.__eq__(other)
