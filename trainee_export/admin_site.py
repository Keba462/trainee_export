from django.contrib.admin import AdminSite as DjangoAdminSite
from django.contrib.sites.shortcuts import get_current_site


class AdminSite(DjangoAdminSite):

    site_header="Trainee Export"
    index_title="Trainee Export"
    enable_nav_sidebar = False
    site_url = '/administration/'

    """def each_context(self, request):
        context = super().each_context(request)
        context.update(global_site=get_current_site(request))
        label = 'Trainee Export'
        context.update(
            site_title=label,
            site_header=label,
            index_title=label,
        )
        return context"""


trainee_export_admin = AdminSite(name='trainee_export_admin')
