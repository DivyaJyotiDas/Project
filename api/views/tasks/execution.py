"""This Class Responsible for returning executionInfo.

Author:- Divya Jyoti Das(divya.das@cumulus-systems.com)
"""
from datetime import datetime
import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
                                    HTTP_200_OK,
                                    HTTP_400_BAD_REQUEST
                                    )

from api.models import Taskgroupexecution
from api.models import TaskExecutionResult
from api.models import Taskgroup
from api.models import Tafv2Task
from api.models import TaskgroupTask
from api.models import Person
from api import apisettings
from api.serializers import TaskExecutionResultSerializers
from api.serializers import TaskgroupTaskSerializers


class ExecutionInfoView(APIView):
    """This class implemnets ExecutionInfo."""

    def getTaskGroupName(tg_id):
        """Will return TaskGroupName related to Id."""
        tg = Taskgroup.objects.get(id=tg_id)
        return tg.name

    def getTasksFromTaskGroup(tg_id, execution_id):
        """Will Return Tasks Name and Id with tg_id."""
        tasks_list = []
        task_exec_result = TaskExecutionResult.objects.filter(
                                                    execution_id=execution_id
                                                    )
        task_exec_data = TaskExecutionResultSerializers(
                                    task_exec_result,
                                    many=True
                                    )

        for i in range(len(task_exec_data.data)):
            result = None
            task_res = dict(task_exec_data.data[i].items())
            task_obj = Tafv2Task.objects.get(id=task_res['task_id'])
            person_obj = Person.objects.get(id=task_obj.author_id)

            if task_res['result'] == 0:
                result = "PASS"
            if task_res['result'] == 1:
                result = "FAIL"
            if task_res['result'] == 2:
                result = "ABORT"
            if task_res['result'] == 3:
                result = "UNKNOWN"
            if task_res['result'] == 4:
                result = "TIMEOUT"

            tasks_list.append({
                                    "taskName": task_obj.script,
                                    "displayName": None if not task_obj.summary else task_obj.summary,
                                    "ownerName": person_obj.name,
                                    "ownerMailID": person_obj.email_address,
                                    "taskId": task_obj.id,
                                    "result": result,
                                    "startTime": task_res['start_time'],
                                    "endTime": task_res['end_time']
                                })
        tasks_list = sorted(tasks_list, key=lambda x : datetime.strptime(x['startTime'], "%Y-%m-%dT%H:%M:%S.%fZ"))
        return tasks_list

    def numTasksScheduled(task_exec_res_data):
        """Return Number Od Tasks Scheduled in TaskGroup Execution."""
        num_tasks_scheduled = len(task_exec_res_data.data)
        return(num_tasks_scheduled)

    def numTasksPassed(task_exec_res_data):
        """Return Number Of numTasksPassed in TaskGroup Execution."""
        num_tasks_passed = 0
        for i in range(len(task_exec_res_data.data)):
            task_res = dict(task_exec_res_data.data[i].items())
            if task_res['result'] == 0:
                num_tasks_passed = num_tasks_passed + 1
        return(num_tasks_passed)

    def numTasksFailed(task_exec_res_data):
        """Return Number Of numTasksFailed in TaskGroup Execution."""
        num_tasks_failed = 0
        for i in range(len(task_exec_res_data.data)):
            task_res = dict(task_exec_res_data.data[i].items())
            if task_res['result'] == 1:
                num_tasks_failed = num_tasks_failed + 1
        return(num_tasks_failed)

    def numTasksAborted(task_exec_res_data):
        """Return Number Of numTasksFailed in TaskGroup Execution."""
        num_tasks_aborted = 0
        for i in range(len(task_exec_res_data.data)):
            task_res = dict(task_exec_res_data.data[i].items())
            if task_res['result'] == 2:
                num_tasks_aborted = num_tasks_aborted + 1
        return(num_tasks_aborted)

    def numTasksUnknown(task_exec_res_data):
        """Return Number numTasksUnknown in TaskGroup Execution."""
        num_tasks_unknown = 0
        for i in range(len(task_exec_res_data.data)):
            task_res = dict(task_exec_res_data.data[i].items())
            if task_res['result'] == 3:
                num_tasks_unknown = num_tasks_unknown + 1
        return(num_tasks_unknown)

    def numTasksTimedOut(task_exec_res_data):
        """Return Number numTasksUnknown in TaskGroup Execution."""
        num_tasks_timed_out = 0
        for i in range(len(task_exec_res_data.data)):
            task_res = dict(task_exec_res_data.data[i].items())
            if task_res['result'] == 4:
                num_tasks_timed_out = num_tasks_timed_out + 1
        return(num_tasks_timed_out)

    def get(self, request):
        """GET will return all Execution Info."""
        execution_list = []
        tg_exec_obj = Taskgroupexecution.objects.all().order_by('-id')[:200]
        for i in tg_exec_obj.iterator():
            task_count = 0
            if i.mode == apisettings.PROD:
                executionStatus = {}
                executionStatus['endTime'] = i.end_time
                executionStatus['startTime'] = i.start_time
                executionStatus['executionName'] = i.name
                executionStatus['executionId'] = i.id
                executionStatus['taskGroupId'] = i.taskgroup_id
                executionStatus['aliasName'] = i.alias_name
                executionStatus['tasks'] = [{}]
                executionStatus['taskResults'] = None
                tg_name = ExecutionInfoView.getTaskGroupName(i.taskgroup_id)
                executionStatus['taskGroupName'] = tg_name

                task_exec_res = TaskExecutionResult.objects.filter(execution_id=i.id)
                task_exec_res_data = TaskExecutionResultSerializers(task_exec_res, many=True)

                tasks_name = ExecutionInfoView.getTasksFromTaskGroup(
                                                                    i.taskgroup_id,
                                                                    i.id
                                                                    )
                executionStatus['tasks'] = tasks_name

                # TODO: This code is for reading Tasks at that time for that tgid.
                # tasksobj = TaskgroupTask.objects.filter(taskgroup_id=i.taskgroup_id)
                # tasks = TaskgroupTaskSerializers(tasksobj, many=True)
                #
                # for o in tasksobj:
                #     task_count += 1

                num_tasks_scheduled = ExecutionInfoView.numTasksScheduled(task_exec_res_data)
                num_tasks_passed = ExecutionInfoView.numTasksPassed(task_exec_res_data)
                num_tasks_failed = ExecutionInfoView.numTasksFailed(task_exec_res_data)
                num_tasks_aborted = ExecutionInfoView.numTasksAborted(task_exec_res_data)
                num_tasks_unknown = ExecutionInfoView.numTasksUnknown(task_exec_res_data)
                num_tasks_timedout = ExecutionInfoView.numTasksTimedOut(task_exec_res_data)
                executionStatus['taskResults'] = {
                    'pass': num_tasks_passed,
                    'fail': num_tasks_failed,
                    'abort': num_tasks_aborted,
                    'unknown': num_tasks_unknown,
                    'timedout': num_tasks_timedout,
                    'total': num_tasks_scheduled
                }

                execution_list.append(executionStatus)

        return Response(execution_list, status=HTTP_200_OK)

    def post(self, request):
        """POST Method is supported and will retirn ExecutionInfo."""
        print(request.data)
        executionStatus = {}
        tg_exec_obj = Taskgroupexecution.objects.get(
                                                id=request.data['executionID']
                                                )
        executionStatus['endTime'] = tg_exec_obj.end_time
        executionStatus['startTime'] = tg_exec_obj.start_time
        executionStatus['executionName'] = tg_exec_obj.name
        executionStatus['taskGroupId'] = tg_exec_obj.taskgroup_id
        executionStatus['tasks'] = [{}]
        executionStatus['taskResults'] = None
        tg_name = ExecutionInfoView.getTaskGroupName(tg_exec_obj.taskgroup_id)
        executionStatus['taskGroupName'] = tg_name
        tasks_name = ExecutionInfoView.getTasksFromTaskGroup(
                                                tg_exec_obj.taskgroup_id,
                                                request.data['executionID']
                                                )
        executionStatus['tasks'] = tasks_name

        task_exec_res = TaskExecutionResult.objects.filter(execution_id=request.data['executionID'])
        task_exec_res_data = TaskExecutionResultSerializers(task_exec_res, many=True)

        num_tasks_scheduled = ExecutionInfoView.numTasksScheduled(task_exec_res_data)
        # executionStatus['taskResults'] = {'unknown': num_tasks_scheduled}

        num_tasks_passed = ExecutionInfoView.numTasksPassed(task_exec_res_data)
        # executionStatus['taskResults'] = {'pass': num_tasks_passed}

        num_tasks_failed = ExecutionInfoView.numTasksFailed(task_exec_res_data)
        # executionStatus['taskResults'] = {'fail': num_tasks_failed}

        num_tasks_aborted = ExecutionInfoView.numTasksAborted(task_exec_res_data)
        # executionStatus['taskResults'] = {'abort': num_tasks_aborted}

        num_tasks_unknown = ExecutionInfoView.numTasksUnknown(task_exec_res_data)

        num_tasks_timedout = ExecutionInfoView.numTasksTimedOut(task_exec_res_data)

        executionStatus['taskResults'] = {
					'pass': num_tasks_passed,
					'fail': num_tasks_failed,
					'abort': num_tasks_aborted,
					'unknown': num_tasks_unknown,
					'timedout': num_tasks_timedout
					}


        return Response(executionStatus, status=HTTP_200_OK)
