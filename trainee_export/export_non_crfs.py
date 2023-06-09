from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
import pandas as pd, datetime, os

from .export_methods import ExportMethods
from .export_model_lists import exclude_fields


class ExportNonCrfData:
    """Export data.
    """

    def __init__(self, export_path=None):
        self.export_path = export_path or django_apps.get_app_config('trainee_export').non_crf_path
        if not os.path.exists(self.export_path):
            os.makedirs(self.export_path)
        self.export_methods_cls = ExportMethods()
        self.rs_cls = django_apps.get_model('edc_registration.registeredsubject')
        self.appointment_cls = django_apps.get_model('edc_appointment.appointment')

    def subject_non_crfs(self, subject_model_list=None, exclude=None, study=None):
        """E.
        """
        for model_name in subject_model_list:
            if 'registeredsubject' == model_name:
                model_cls = self.rs_cls
            elif 'appointment' == model_name:
                model_cls = self.appointment_cls
            else:
                model_cls = django_apps.get_model(study, model_name)
            objs = model_cls.objects.all()
            count = 0
            models_data = []

            for obj in objs:
                data = self.export_methods_cls.fix_date_format(self.export_methods_cls.non_crf_obj_dict(obj=obj))
                if exclude:
                    exclude_fields.append(exclude)

                for e_fields in exclude_fields:
                    try:
                        del data[e_fields]
                    except KeyError:
                        pass
                models_data.append(data)
                count += 1
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            fname = f'{study}_' + model_name + '_' + timestamp + '.csv'
            final_path = self.export_path + fname
            df_crf = pd.DataFrame(models_data)
            df_crf.rename(columns={'subject_identifier':
                                   'subject_identifier'}, inplace=True)
            df_crf.to_csv(final_path, encoding='utf-8', index=False)

   

    def offstudy(self, offstudy_prn_model_list=None):
        """Export off study forms.
        """

        for model_name in offstudy_prn_model_list:
            model_cls = django_apps.get_model('trainee_prn', model_name)
            objs = model_cls.objects.all()
            count = 0
            models_data = []
            for obj in objs:
                data = obj.__dict__
                data = self.export_methods_cls.encrypt_values(data, obj.__class__)
                try:
                    rs = self.rs_cls.objects.get(subject_identifier=obj.subject_identifier)
                except self.rs_cls.DoesNotExist:
                    raise ValidationError('Registered subject can not be missing')
                else:
                    if not 'dob' in data:
                        data.update(dob=rs.dob)
                    if not 'gender' in data:
                        data.update(gender=rs.gender)
                    if not 'screening_identifier' in data:
                        data.update(screening_identifier=rs.screening_identifier)
                    data.update(
                        relative_identifier=rs.relative_identifier,
                        screening_age_in_years=rs.screening_age_in_years,
                        registration_datetime=rs.registration_datetime
                    )
                last_data = self.export_methods_cls.fix_date_format(data)
                for e_fields in exclude_fields:
                    try:
                        del last_data[e_fields]
                    except KeyError:
                        pass
                models_data.append(last_data)
                count += 1
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            fname = 'trainee_prn_' + model_name + '_' + timestamp + '.csv'
            final_path = self.export_path + fname
            df_crf = pd.DataFrame(models_data)
            df_crf.to_csv(final_path, encoding='utf-8', index=False)

    def death_report(self, death_report_prn_model_list=None):
        for model_name in death_report_prn_model_list:
            model_cls = django_apps.get_model('trainee_prn', model_name)
            objs = model_cls.objects.all()
            count = 0
            models_data = []
            for obj in objs:
                data = obj.__dict__
                try:
                    rs = self.rs_cls.objects.get(subject_identifier=obj.subject_identifier)
                except self.rs_cls.DoesNotExist:
                    raise ValidationError('Registered subject can not be missing')
                else:
                    if not 'dob' in data:
                        data.update(dob=rs.dob)
                    if not 'gender' in data:
                        data.update(gender=rs.gender)
                    if not 'screening_identifier' in data:
                        data.update(screening_identifier=rs.screening_identifier)
                    data.update(
                        relative_identifier=rs.relative_identifier,
                        screening_age_in_years=rs.screening_age_in_years,
                        registration_datetime=rs.registration_datetime
                    )
                data = self.export_methods_cls.encrypt_values(data, obj.__class__)
                last_data = self.export_methods_cls.fix_date_format(data)
                for e_fields in exclude_fields:
                    try:
                        del last_data[e_fields]
                    except KeyError:
                        pass
                models_data.append(last_data)
                count += 1
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            fname = 'trainee_prn_' + model_name + '_' + timestamp + '.csv'
            final_path = self.export_path + fname
            df_crf = pd.DataFrame(models_data)
            df_crf.to_csv(final_path, encoding='utf-8', index=False)

    def subject_visit(self):

        subject_visits = django_apps.get_model('trainee_subject.sbjectvisit').objects.all()
        data = []
        for mv in subject_visits:
            d = mv.__dict__
            d = self.export_methods_cls.fix_date_format(d)
            for e_fields in exclude_fields:
                try:
                    del d[e_fields]
                except KeyError:
                    pass
            data.append(d)
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        fname = 'trainee_subject_subject_visit' + '_' + timestamp + '.csv'
        final_path = self.export_path + fname
        df_crf = pd.DataFrame(data)
        df_crf.to_csv(final_path, encoding='utf-8', index=False)

    