"""apiexample URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.csrf import csrf_exempt
from api.views.ui import dashboard
from api.views.ui import  index

urlpatterns = [
    # TaskGroup related API's
    url(r'^$', index.LoginView),
    url(r'^home$', index.HomeView, name = 'home'),
    url(r'^tasks$', index.TasksView, name = 'tasks'),
    url(r'^taskgroup$', index.TaskgroupView, name = 'taskgroup'),
    url(r'^logout$', index.LogoutView, name = 'logout'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
