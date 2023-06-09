from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings
import datetime
from edc_base.apps import AppConfig as BaseEdcBaseAppConfig
from edc_device.apps import AppConfig as BaseEdcDeviceAppConfig
from edc_device.constants import CENTRAL_SERVER

class AppConfig(DjangoAppConfig):
    name = 'trainee_export'
    verbose_name = 'Trainee Export'
    today_date = datetime.datetime.now().strftime('%Y%m%d')
    export_date =  '/documents/trainee_export_' + today_date
    subject_path = settings.MEDIA_ROOT + export_date + '/subject/'
    non_crf_path = settings.MEDIA_ROOT + export_date + '/non_crf/'
    admin_site_name = 'trainee_export_admin'



class EdcBaseAppConfig(BaseEdcBaseAppConfig):
    project_name = 'Trainee Export'
    institution = 'Botswana-Harvard AIDS Institute'


class EdcDeviceAppConfig(BaseEdcDeviceAppConfig):
    device_role = CENTRAL_SERVER
    device_id = '99'
