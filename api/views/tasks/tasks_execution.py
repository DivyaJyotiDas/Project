"""This view executes the api and return the response code with message.

Author:- Divya Jyoti Das(divya.das@cumulus-systems.com)
Api:- api/taskGroup/execute
body:- {
            "taskGroupName": ["taskGroupName"]
        }
Response:- {
                "executionID": 370
            }
"""

import time
from datetime import datetime
import pytz

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
                                    HTTP_200_OK,
                                    HTTP_400_BAD_REQUEST
                                  )
from api.validation.taskgroup_execution_validation import (
                                                TaskGroupExecutionValidation,
                                                        )
from api.models import Taskgroup
from api.models import Tafv2Task
from api.models import TaskgroupTask
from api.serializers import TaskgroupSerializers
from api.serializers import TaskgroupTaskSerializers


class TaskGroupExecuteView(APIView):
    """TaskGroupExecuteView is for executiong taskGroupName passed in api.

    methods:-
    1. get():

    2. post():

    """

    def get(self, request):
        """Get method is a verb. As of now we dont support it."""
        return Response(
                        {
                            "GET": "Not supported",
                            "POST": "Supported"
                        },
                        status=HTTP_400_BAD_REQUEST
                        )

    def post(self, request):
        """Post method is a verb.

        Api:- api/taskGroup/execute
        body:- {
                "taskGroupName" : ["TG-1"]
                }
        Response:- if TaskGroup exist
                    200
                    else
                    400
                    {status": "Task-Group Doesn't Exist.Pls create one.}

        """
        logger = Log.get_logger(__name__)
        logger.info("Framework:: execute API Hits with parameter %s", request.data)
        global_context = request.data
        context = {}
        setup = None
        valid = TaskGroupExecutionValidation(request.data, request.FILES)
        if valid.is_valid():
            try:
                if request.data.get('taskGroupName'):
                    tg_name = request.data['taskGroupName'][0]
                    setup = TaskGroupExecuteView.getSetup(request)
                    all_taskgroup_objects = Taskgroup.objects.get(name=tg_name)
                    if all_taskgroup_objects:
                        context = TaskGroupExecuteView.getTGTasksName(all_taskgroup_objects, tg_name)
                        new_entry_response = ExecTasks.executeTasksList(
                                                            context['tgList'],
                                                            context['tasksList'],
                                                            global_context,
                                                            setup
                                                            )
                        return Response(new_entry_response)
                    else:
                        return Response("No TG with this name")
                elif request.data.get('tasks'):
                    is_exist = TaskGroupExecuteView.isTasksExists(request)
                    if is_exist.get('taskResult'):
                        setup = TaskGroupExecuteView.getSetup(request)
                        datetime = TaskGroupExecuteView.getHumanReadableDateTime()
                        tg = Taskgroup(
                                name='TG-'+datetime
                                    )
                        tg.save()
                        all_taskgroup_objects = Taskgroup.objects.get(name=tg.name)
                        tasks_ids = TaskGroupExecuteView.getTaskIdsFromName(request.data['tasks'])
                        status = TaskGroupExecuteView.createRelationBetweenTGTasks(tg.id, tasks_ids)
                        if status:
                            context = TaskGroupExecuteView.getTGTasksName(all_taskgroup_objects, tg.name)
                            new_entry_response = ExecTasks.executeTasksList(
                                                                context['tgList'],
                                                                context['tasksList'],
                                                                global_context,
                                                                setup
                                                                )
                        return Response(new_entry_response)
                    else:
                        return Response(
                                        is_exist['taskStatus'],
                                        status=HTTP_400_BAD_REQUEST
                                        )
                else:
                    context['status'] = "Task-Group Doesn't Exist.Pls create one."
                    return Response(context, status=HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response(e)
        else:
            context['status'] = 'Invalid input'
            return Response(context, status=HTTP_400_BAD_REQUEST)

    def getSetup(request):
        """Will Return Setup Details if provided."""
        setup = None
        if request.data.get("setup"):
            setup = request.data['setup']
        return setup

    def isTasksExists(request):
        """Will Determine wether Tasks Exists or Not."""
        task_status = {}
        task_result = 0
        flag = None
        for task in request.data['tasks']:
            task_obj = Tafv2Task.objects.filter(script=task)
            if task_obj:
                task_status[task] = "Task Exists."
            else:
                task_result += 1
                task_status[task] = "Task doesn't Exists."
        if task_result > 0:
            flag = False
        else:
            flag = True

        return {'taskResult': flag, 'taskStatus': task_status}

    def getTaskIdsFromName(tasks_name):
        """Get Tasks IDs From TaskName."""
        ids = []
        for name in tasks_name:
            task_obj = Tafv2Task.objects.get(script=name)
            ids.append(task_obj.id)

        return ids

    def createRelationBetweenTGTasks(tg_id, tasks_ids):
        """Will create Relation Between TaskGroup and Task Table."""
        tg_tasks_obj = None
        tgid = Taskgroup.objects.get(id=tg_id)
        for tid in tasks_ids:
            tg_tasks_obj = TaskgroupTask(
                                taskgroup=tgid,
                                task_id=tid  # Task.objects.get(id=tid)
                                    )
            tg_tasks_obj.save()
        if tg_tasks_obj.id:
            return True
        else:
            return False

    def getTGTasksName(all_taskgroup_objects, tg_name):
        """Will Return TaskGroup and Task Name to be sent to ExecTasks."""
        tg_id = all_taskgroup_objects.id
        tg_task_obj = TaskgroupTask.objects.filter(
                                        taskgroup_id=tg_id
                                        )
        tg_task = TaskgroupTaskSerializers(
                                    tg_task_obj,
                                    many=True
                                    )
        tasks_list = []
        tg_list = []
        try:
            for i in range(len(tg_task.data)):
                tasks = dict(tg_task.data[i].items())
                print("#############", tasks)
                task_obj = Tafv2Task.objects.get(id=tasks['task_id'])
                tasks_list.append({
                                    "task_name": task_obj.script,
                                    "task_id": task_obj.id
                                })
            tg_list.append({
                            "tg_name": tg_name,
                            "tg_id": tg_id
                            })

            context = {'tgList': tg_list, 'tasksList': tasks_list}
            print("$$$$$$$$$$$$$$", context)
            return context
        except Exception as e:
            print(e)

    def getHumanReadableDateTime():
        """Will Returns Human Readable DateTime."""
        date = str(datetime.now(tz=pytz.UTC))
        date = date.replace(' ', '_')
        date = date.split(".")[0]
        return date
