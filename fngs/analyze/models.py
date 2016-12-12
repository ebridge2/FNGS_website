from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
import os.path as op
import os
import uuid


def get_func_file_path(instance, filename):
	# extension is everything after first period
	return os.path.join("/".join([str(instance.dataset), str(instance.sub_id), str(instance.sess_id), "func", filename]))
def get_anat_file_path(instance, filename):
	return os.path.join("/".join([str(instance.dataset), str(instance.sub_id), str(instance.sess_id), "anat", filename]))

def get_dti_file_path(instance, filename):
	return os.path.join("/".join([str(instance.dataset), str(instance.sub_id), str(instance.sess_id), "dti", filename]))

def get_mprage_file_path(instance, filename):
	return os.path.join("/".join([str(instance.dataset), str(instance.sub_id), str(instance.sess_id), "mprage", filename]))

def get_bvals_file_path(instance, filename):
	return os.path.join("/".join([str(instance.dataset), str(instance.sub_id), str(instance.sess_id), "bvals", filename]))

def get_bvecs_file_path(instance, filename):
	return os.path.join("/".join([str(instance.dataset), str(instance.sub_id), str(instance.sess_id), "bvecs", filename]))

def get_labels_file_path(instance, filename):
	return os.path.join("/".join([str(instance.dataset), str(instance.sub_id), str(instance.sess_id), "labels", filename]))

class Dataset(models.Model):
	dataset_id = models.CharField(max_length=30)
	collection_site = models.CharField(max_length=40)
	output_url = models.CharField(max_length=200, null=True, blank=True)

	def add_output_url(self, url):
		output_url = models.TextField(url)
			
	def __str__(self):
		return str(self.dataset_id)

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.dataset_id == other.dataset_id
		return False

	def __ne__(self, other):
		return not self.__eq__(other)


class Subject(models.Model):
	dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
	sub_id = models.CharField(max_length=30)
	sess_id = models.CharField(max_length=30)
	struct_scan = models.FileField(upload_to=get_anat_file_path, null=True, blank=True)
	func_scan = models.FileField(upload_to=get_func_file_path, null=True, blank=True)
	output_url = models.CharField(max_length=200, null=True, blank=True)
	STC_CHOICES = (
		(None, 'None'),
		('up', 'Bottom Up Acquisition (standard)'),
		('down', 'Top Down Acquisition'),
		("interleaved", 'Interleaved Acquisition')
	)
	slice_timing = models.CharField(max_length=20, choices=STC_CHOICES)
	AN_CHOICES = (
		(1, 'T1w'),
		(2, 'T2w'),
		(3, 'PD')
	)
	an = models.IntegerField(choices=AN_CHOICES, default=1)
	dti_file = models.FileField(upload_to=get_dti_file_path, null=True, blank=True)
	bvals_file = models.FileField(upload_to=get_bvals_file_path, null=True, blank=True)
	bvecs_file = models.FileField(upload_to=get_bvecs_file_path, null=True, blank=True)

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return ((self.dataset == other.dataset) and (self.sub_id == other.sub_id))
		return False

	def get_id(self):
		return str(op.splitext(op.splitext(op.basename(self.func_scan.name))[0])[0])

	def __ne__(self, other):
		return not self.__eq__(other)

	def add_output_url(self, url):
		output_url = models.TextField(url)

	def __str__(self):
		return str(str(self.dataset) + "_" + str(self.sub_id))
