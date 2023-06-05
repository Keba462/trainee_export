"""trainee_export URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from edc_dashboard import UrlConfig
from trainee_export.views.home_view import HomeView
from trainee_export.views.listboard_view import ListBoardView

from .patterns import export_identifier
from .admin_site import *

app_name = 'trainee_export'

urlpatterns = [
    path('admin/', trainee_export_admin.urls),
    path('', HomeView.as_view(), name='home_url'),
]



export_listboard_url_config = UrlConfig(
    url_name='export_listboard_url',
    view_class=ListBoardView,
    label='export_listboard',
    identifier_label='export_identifier',
    identifier_pattern=export_identifier)


urlpatterns += export_listboard_url_config.listboard_urls
