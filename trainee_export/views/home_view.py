import datetime
import re
import threading
import time

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from trainee_export.views.listboard_view_mixin import ListBoardViewMixin
from trainee_export.models.export_file import ExportFile

from ..identifiers import ExportIdentifier



class HomeView(ListBoardViewMixin, EdcBaseViewMixin,
               NavbarViewMixin, TemplateView):

    template_name = 'trainee_export/home.html'
    navbar_name = 'trainee_export'
    navbar_selected_item = 'study_data_export'
    identifier_cls = ExportIdentifier

    def stop_main_thread(self, thread_name):
        """Stop export file generation thread.
        """
        time.sleep(20)
        threads = threading.enumerate()
        threads = [t for t in threads if t.is_alive()]
        for thread in threads:
            if thread.name == thread_name:
                thread._stop()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        download = self.request.GET.get('download')

        if download == '2':
            self.generate_export(thread_name='trainee_non_crf_export',
                                 thread_target=self.download_non_crf_data,
                                 description='Trainee Non CRF Export')
        elif download == '3':
            self.generate_export(thread_name='trainee_subject_crf_export',
                                 thread_target=self.download_subject_data,
                                 description='Trainee Subject CRF Export')
        non_crf_exports = ExportFile.objects.filter(
            description='Trainee Non CRF Export').order_by('-uploaded_at')[:10]
        subject_crf_exports = ExportFile.objects.filter(
            description='Trainee Subject CRF Export').order_by('-uploaded_at')[:10]
       
        #breakpoint()
        context.update(
            non_crf_exports=non_crf_exports,
            subject_crf_exports=subject_crf_exports,
            )
        return context

    def generate_export(self, thread_name=None, active_download=False,
                        thread_target=None, description=None):

        threads = threading.enumerate()

        if threads:
            for thread in threads:
                if thread.name == thread_name:
                    active_download = True
                    messages.add_message(
                        self.request, messages.INFO,
                        (f'Download for {description} that was initiated is still running '
                         'please wait until an export is fully prepared.'))

        if not active_download:
            is_clean = self.is_clean(description=description)
            if is_clean:

                #breakpoint()

                download_thread = threading.Thread(
                    name=thread_name, target=thread_target,
                    daemon=True)
                download_thread.start()
                last_doc = ExportFile.objects.filter(description=description,download_complete=True).order_by('created').last()

                if last_doc:
                    start_time = datetime.datetime.now().strftime(
                        "%d/%m/%Y %H:%M:%S")
                    last_doc_time = round(
                        float(last_doc.download_time) / 60.0, 2)

                    messages.add_message(
                        self.request, messages.INFO,
                        (f'Download for {description}has been initiated, you will receive an email once '
                         'the download is completed. Estimated download time: '
                         f'{last_doc_time} minutes, file generation started at:'
                         f' {start_time}'))
                else:
                    messages.add_message(
                        self.request, messages.INFO,
                        (f'Download for {description} initiated, you will receive an email once '
                         'the download is completed.'))
                    

        
