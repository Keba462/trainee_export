import datetime
import re
from unittest import result

from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django_crypto_fields.fields import (
    EncryptedCharField, EncryptedDecimalField, EncryptedIntegerField,
    EncryptedTextField, FirstnameField, IdentityField, LastnameField)
from pytz import timezone

encrypted_fields = [
    EncryptedCharField, EncryptedDecimalField, EncryptedIntegerField,
    EncryptedTextField, FirstnameField, IdentityField, LastnameField]


class ExportMethods:
    """Export Trainee data.
    """

    trainee_offstudy_model = 'trainee_prn.subjectoffstudy'
   

    @property
    def subject_offstudy_cls(self):
        return django_apps.get_model(self.trainee_offstudy_model)



    def __init__(self):
        self.rs_cls = django_apps.get_model('edc_registration.registeredsubject')
        self.subject_consent_csl = django_apps.get_model('trainee_subject.subjectconsent')

    def encrypt_values(self, obj_dict=None, obj_cls=None):
        """Ecrypt values for fields that are encypted.
        """
        result_dict_obj = {**obj_dict}
        for key, value in obj_dict.items():
            for f in obj_cls._meta.get_fields():
                if key == f.name and type(f) in encrypted_fields:
                    new_value = f.field_cryptor.encrypt(value)
                    result_dict_obj[key] = new_value
        return result_dict_obj

    def onstudy_value(self, subject_identifier, is_subject):
        """
        This method is used to check if the subject identifier is offstudy
        subject_identifier - specify is the participant is offstudy
        is_subject - should be true if the subject identifier is from a subject, 
        otherwise false 
        """

        # is should always be initialized
        if is_subject is None:
            raise TypeError(
                'is_subject cannot be null, value should either be True or False')

        # Value constants
        ON_STUDY = 'On Study'
        OFF_STUDY = 'Off Study'

        # when an exception is thrown it means the subject is offstudy
        # or inversly they are both onstudy
        if is_subject:
            try:
                self.subject_offstudy_cls.objects.get(subject_identifier=subject_identifier)
            except self.subject_offstudy_cls.DoesNotExist:
                result = ON_STUDY
            else:
                result = OFF_STUDY

        return result

    def fix_date_format(self, obj_dict=None):
        """Change all dates into a format for the export
        and split the time into a separate value.

        Format: m/d/y
        """

        result_dict_obj = {**obj_dict}
        for key, value in obj_dict.items():
            if isinstance(value, datetime.datetime):
                value = value.astimezone(timezone('Africa/Gaborone'))
                time_value = value.time().strftime('%H:%M:%S.%f')
                time_variable = None
                if 'datetime' in key:
                    time_variable = re.sub('datetime', 'time', key)
                else:
                    time_variable = key + '_time'
                value = value.strftime('%m/%d/%Y')
                new_key = re.sub('time', '', key)
                result_dict_obj[new_key] = value
                del result_dict_obj[key]
                result_dict_obj[time_variable] = time_value
            elif isinstance(value, datetime.date):
                value = value.strftime('%m/%d/%Y')
                result_dict_obj[key] = value
        return result_dict_obj

    def subject_crf_data_dict(self, crf_obj=None):
        """Return a crf obj dict adding extra required fields.
        """

        data = crf_obj.__dict__
        data = self.encrypt_values(obj_dict=data, obj_cls=crf_obj.__class__)
        data.update(
            subject_identifier=crf_obj.subject_visit.subject_identifier,
            visit_datetime=crf_obj.subject_visit.report_datetime,
            last_alive_date=crf_obj.subject_visit.last_alive_date,
            reason=crf_obj.subject_visit.reason,
            survival_status=crf_obj.subject_visit.survival_status,
            visit_code=crf_obj.subject_visit.visit_code,
            visit_code_sequence=crf_obj.subject_visit.visit_code_sequence,
            study_status=crf_obj.subject_visit.study_status,
            appt_status=crf_obj.subject_visit.appointment.appt_status,
            appt_datetime=crf_obj.subject_visit.appointment.appt_datetime,
            status=self.onstudy_value(
                subject_identifier=crf_obj.subject_visit.subject_identifier,
                is_subject=True,
            )
        )
        try:
            rs = self.rs_cls.objects.get(subject_identifier=crf_obj.subject_visit.subject_identifier)
        except self.rs_cls.DoesNotExist:
            raise ValidationError('RegisteredSubject can not be missing')
        else:
            data.update(
                screening_age_in_years=rs.screening_age_in_years,
                registration_status=rs.registration_status,
                dob=rs.dob,
                gender=rs.gender,
                subject_type=rs.subject_type,
                registration_datetime=rs.registration_datetime,
            )
        return data

    

    def non_crf_obj_dict(self, obj=None):
        """Return a dictionary of non crf object.
        """

        data = obj.__dict__
        data = self.encrypt_values(obj_dict=data, obj_cls=obj.__class__)
        if 'subject_identifier' in data:
            subject_consent = self.subject_consent_csl.objects.filter(
                subject_identifier=obj.subject_identifier).last()

            if subject_consent:
                if 'dob' not in data:
                    data.update(dob=subject_consent.dob)
                if 'gender' in data:
                    data.update(gender=subject_consent.gender)
                if 'screening_identifier' not in data:
                    data.update(screening_identifier=subject_consent.screening_identifier)

            if 'registration_datetime' not in data:
                try:
                    rs = self.rs_cls.objects.get(subject_identifier=obj.subject_identifier)
                except self.rs_cls.DoesNotExist:
                    data.update(
                        registration_datetime=None,
                        screening_datetime=None
                    )
                else:
                    data.update(
                        registration_datetime=rs.registration_datetime,
                        screening_datetime=rs.screening_datetime
                    )
        else:
            if 'screening_identifier' not in data:
                data.update(screening_identifier=None)
            data.update(
                screening_age_in_years=None,
                dob=None,
                gender=None,

            )

        return data
