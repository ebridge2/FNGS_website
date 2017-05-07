from django import forms
from django.contrib.auth.models import User
from .models import QuerySubmission
from django.utils.translation import ugettext_lazy as _


class QuerySubmissionForm(forms.ModelForm):
	class Meta:
		model = QuerySubmission
		fields = ['state', 'bucket', 'bidsdir', 'jobdir', 'creds_file', 'datasetname', 'modality', 'slice_timing']
		labels={
			'state':_('Analysis Level'),
			'bucket':_('S3 Bucket Name'),
			'bidsdir':_('S3 Bucket BIDS Directory'),
			'jobdir':_('Job Directory'),
			'creds_file':_('AWS Credentials File'),
			'datasetname':_('Dataset Name'),
			'modality':_('Modality'),
			'slice_timing':_('Slice Timing Method')
		}
		help_texts={
			'state':_('Level of analysis to perform'),
			'bucket':_('Name of S3 bucket where data lives'),
			'bidsdir':_('Path on S3 bucket where data lives'),
			'jobdir':_('Directory of jobs to kill or check status'),
			'creds_file':_('File containing user credentials for AWS services'),
			'datasetname':_('Dataset name'),
			'modality':_('Modality of data'),
			'slice_timing':_('The method in which slices were acquired.')
		}
