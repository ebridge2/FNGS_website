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
			'state':_('Type of query you wish to perform on your jobs'),
			'jobdir':_('The personalized unique identifier that you used to submit the jobs originally.'),
			'creds_file':_('CSV file containing your user credentials for AWS services')
		}
