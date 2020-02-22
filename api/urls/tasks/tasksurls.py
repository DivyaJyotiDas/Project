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
from api.views.tasks.esxViews import *
from api.views.tasks.tasks_views import *

# router = routers.DefaultRouter()
#
# router.register("TaskGroupExecutionSetup", SetupView)
#from api.views import RPMInstallView, ZipUpgradeHDCA

urlpatterns = [
    # TaskGroup related API's
    url(r'^api/taskGroup/create', csrf_exempt(TaskGroupCreateView.as_view())),  # create TaskGroup and stores in DB.
    url(r'^api/taskGroup/getTaskGroupInfo', csrf_exempt(TaskGroupInfoView.as_view())),

    # list all TaskGroup from DB as JSON.
    url(r'^api/taskGroup/execute', csrf_exempt(TaskGroupExecuteView.as_view())),  # Executes TaskGroup one-by-one

    # shows Execution Info of TaskGroup.
    url(r'^api/taskGroup/executionInfo', csrf_exempt(TaskGroupExecutionInfoView.as_view())),

    # Task Related Api
    url(r'^api/task/result', csrf_exempt(ResultView.as_view())),
    url(r'^api/task/create', csrf_exempt(TaskCreateView.as_view())),
    url(r'^api/task/info', csrf_exempt(TaskInfoView.as_view())),
]
urlpatterns = format_suffix_patterns(urlpatterns)
