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
from api.views.tasks.tasks_execution import TaskGroupExecuteView
from api.views.tasks.task_create import TaskGroupCreateView, TaskGroupListView
from api.views.tasks.task_result import ResultView
from api.views.tasks.execution import ExecutionInfoView
from api.views.ui.testcases_tracker_view import TestCasesTrackView


urlpatterns = [
    url(r'^api/testCases/add', csrf_exempt(TestCasesTrackView.as_view())),
    url(r'^api/testCases/add', csrf_exempt(TestCasesTrackView.as_view())),
    url(r'^api/testCases/list', csrf_exempt(TestCasesTrackView.as_view())),
    url(r'^api/testCases/edit', csrf_exempt(TestCasesTrackView.as_view())),
    url(r'^api/taskGroup/execute', csrf_exempt(TaskGroupExecuteView.as_view())),
    #url(r'^api/task/update', csrf_exempt(TaskUpdateView.as_view())),
    url(r'^api/taskgroup/list', csrf_exempt(TaskGroupListView.as_view())),
    url(r'^api/taskGroup/create', csrf_exempt(TaskGroupCreateView.as_view())),
    url(r'^api/task/result', csrf_exempt(ResultView.as_view())),
    url(r'^api/execution/getInfo', csrf_exempt(ExecutionInfoView.as_view())),
                ]

urlpatterns = format_suffix_patterns(urlpatterns)
