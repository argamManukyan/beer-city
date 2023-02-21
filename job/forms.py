from django import forms
from job.models import SubmittedResumes, CustomResumeForJob


class SubmitFileForm(forms.ModelForm):
    class Meta:
        model = SubmittedResumes
        fields = "__all__"


class CustomCVForm(forms.ModelForm):
    class Meta:
        model = CustomResumeForJob
        exclude = ['phone', 'gender']