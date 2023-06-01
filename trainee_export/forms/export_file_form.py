from django import forms
from trainee_export.models.export import ExportFile


class ExportFileForm(forms.ModelForm):
    class Meta:
        model = ExportFile
        fields = ('description', 'document', )