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

class QuerySubmission(models.Model):
	output_url = models.CharField(max_length=200, null=True, blank=True)
	STATE_CHOICES = (
		('status', 'Job status'),
		('kill', 'Kill jobs')
	)
	state = models.CharField(max_length=20, choices=STATE_CHOICES)
	jobdir = models.CharField(max_length=100, blank=True)
	creds_file = models.FileField(upload_to=get_creds_file_path, null=True, blank=True)

	def add_output_url(self, url):
		output_url = models.TextField(url)
			
	def __str__(self):
		return str(self.jobdir)

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return (self.jobdir == other.jobdir)
		return False

	def __ne__(self, other):
		return not self.__eq__(other)
