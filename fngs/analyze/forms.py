from django import forms
from django.contrib.auth.models import User
from .models import Submission
from django.utils.translation import ugettext_lazy as _


class SubmissionForm(forms.ModelForm):
	class Meta:
		model = Submission
		fields = ['state', 'bucket', 'bidsdir', 'jobdir', 'creds_file', 'datasetname', 'modality', 'slice_timing', 'data_file', 'upload_data_or_not']
		labels={
			'state':_('Analysis Level'),
			'bucket':_('S3 Bucket Name'),
			'bidsdir':_('BIDS Directory'),
			'jobdir':_('Unique Token'),
			'creds_file':_('AWS Credentials File'),
			'datasetname':_('Dataset Name'),
			'modality':_('Modality'),
			'slice_timing':_('Slice Timing Method'),
			'data_file':_('Local Data (Zipped)'),
			'upload_data_or_not':_('Upload Local Data?')
		}
		help_texts={
			'state':_('Level of analysis you want to perform'),
			'bucket':_('Name of the S3 bucket where your data lives'),
			'bidsdir':_("Path on the S3 bucket where data lives (root folder of BIDS spec'd data)"),
			'jobdir':_('Your personalized unique identifier that you can use later for queries'),
			'creds_file':_('CSV file containing your user credentials for AWS services'),
			'datasetname':_('Dataset name (only for group analysis)'),
			'modality':_('Modality of the data'),
			'slice_timing':_('The method in which the data slices were acquired'),
			'data_file':_('Local data that you want to uploaded to the specified S3 bucket before running analysis (zipped at one level above BIDS root)'),
			'upload_data_or_not':_("Whether or not the local data should be uploaded to S3 (select 'No' if you haven't selected a file above)")
		}
