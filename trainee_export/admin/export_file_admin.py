from django.contrib import admin
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base.sites.admin import ModelAdminSiteMixin
from edc_model_admin import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin,
    ModelAdminRedirectOnDeleteMixin)
from edc_model_admin import audit_fieldset_tuple
from edc_subject_dashboard import ModelAdminSubjectDashboardMixin
from trainee_export.forms.export_file_form import ExportFileForm
from trainee_export.models.export_file import ExportFile
from ..admin_site import trainee_export_admin




class ModelAdminMixin(ModelAdminNextUrlRedirectMixin,
                      ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
                      ModelAdminInstitutionMixin,
                      ModelAdminRedirectOnDeleteMixin,
                      ModelAdminSubjectDashboardMixin, ModelAdminSiteMixin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'


@admin.register(ExportFile, site=trainee_export_admin)
class ExportFileAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ExportFileForm

    fieldsets = (
        (None, {
            'fields': (
                'description',
                'document',
                'study',
                'download_time',
                'download_complete')}),
        audit_fieldset_tuple
    )

    search_fields = ['export_identifier']

    list_display = ('export_identifier', 'description', 'download_time',
                    'download_complete',)

    list_filter = ('download_complete', 'description',)
