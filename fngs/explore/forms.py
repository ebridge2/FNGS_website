from django import forms
from django.contrib.auth.models import User
from .models import QuerySubmission
from django.utils.translation import ugettext_lazy as _


class QuerySubmissionForm(forms.ModelForm):
	class Meta:
		model = QuerySubmission
		fields = ['state', 'jobdir', 'creds_file']
		labels={
			'state':_('Query type'),
			'jobdir':_('Unique token'),
			'creds_file':_('AWS Credentials File')
		}
		help_texts={
			'state':_('Level of analysis to perform'),
			'jobdir':_('Unique token of jobs to kill or check status'),
			'creds_file':_('File containing user credentials for AWS services')
		}
