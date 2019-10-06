"""Helper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from Helper.mainlog import Index,Get_Data,Set_Data,Page_Return_Data,Any_Page,Backup,Webstat
urlpatterns = [
    url(r'^backup/$', Backup),
    url(r'^getdata/$', Get_Data),
    url(r'^setdata/$', Set_Data),
    url(r'^pages/(.*)', Page_Return_Data),
    url(r'^webstat$', Webstat),
    url(r'^index$', Index),
    url(r'^$', Index),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico', permanent=True)),
    #url(r'^.*$', Any_Page),

]
