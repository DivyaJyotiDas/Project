"""This Class is Responsible for creating TaskGroup.

Author:- Divya Jyoti Das(divya.das@cumulus-systems.com)
This will also create Relation Between TaskGroup-Task.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
                                    HTTP_200_OK,
                                    HTTP_400_BAD_REQUEST
                                    )

from api.validation.taskgroup_create_validation import (
                                                TaskGroupCreateValidation
                                                        )
from api.models import Taskgroup
from api.models import TaskgroupTask
from api.models import Tafv2Task
from api.models import Person

from api.serializers import Tafv2TaskSerializers
from api.serializers import TaskgroupSerializers


class TaskGroupCreateView(APIView):
    """This View will create TaskGroup and store in TaskGroup DB with relations.

    Api:- api/taskGroup/create
    Body:- {
                "taskGroup": [
                        {
                            "taskGroupName": "TG-1",
                            "tasks": ["t1","t2","t3"]
                        },
                        {
                            "taskGroupName": "TG-1",
                            "tasks": ["t1","t2","t3"]
                        }                    ]
            }
    """

    def createAutoTaskGroup(self, request):
        pass

    def get(self, request):
        """GET Method is not supported."""
        print("In Get")
        return Response(status=HTTP_400_BAD_REQUEST)

    def post(self, request):
        """POST Method is for creating TaskGroup and Relation."""
        msg = {}
        all_tasks_in_tg = None
        tg_create_obj = TaskGroupCreateValidation(request.data, request.FILES)
        # TODO:- Add validation which is not implemented yet.
        if True:  # not tg_create_obj.is_valid():
            for num_tasks in range(len(request.data['taskGroups'])):
                list_of_task_ids = []
                tg_name = request.data['taskGroups'][num_tasks]['taskGroupName']
                author = request.data.get('author', None)
                added_at = request.data.get('addedAt', None)
                tg_tasks = request.data['taskGroups'][num_tasks]['tasks']
                all_tg_obj = Taskgroup.objects.all().filter(name=tg_name)

                if all_tg_obj:
                    msg[tg_name] = "Failed. Already Exists."
                else:
                    msg[tg_name] = {}
                    task_failed = 0
                    for task in tg_tasks:
                        try:
                            all_tasks_in_tg = Tafv2Task.objects.all(). \
                                                        filter(
                                                            script=task
                                                            )
                            task_ids = Tafv2TaskSerializers(
                                                    all_tasks_in_tg,
                                                    many=True
                                                        )

                            task_ids = dict(task_ids.data[0].items())
                            list_of_task_ids.append(task_ids['id'])
                        except Exception as e:
                            print(e)
                        if not all_tasks_in_tg:
                            task_failed = task_failed + 1
                            msg[tg_name][task] = "Task Doesnt Exist. \
                                                    pls create one."
                    if task_failed == 0:
                        per_obj = Person.objects.get(name=author)
                        tg = Taskgroup(
                                name=tg_name,
                                author_id=per_obj.id,
                                last_modified_by=author,
                                added_at=added_at,
                                last_updated_at = added_at
                                )
                        tg.save()
                        tgid = Taskgroup.objects.latest('id')
                        print(list_of_task_ids)
                        for tid in list_of_task_ids:
                            tg_tasks_obj = TaskgroupTask(
                                                taskgroup=tgid,
                                                task_id=tid  # Task.objects.get(id=tid)
                                                    )
                            tg_tasks_obj.save()
                        msg[tg_name] = "Passed. Created"
            return Response({"status": msg}, status=HTTP_200_OK)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)


class TaskGroupListView(APIView):
    def get(self, request):
        """GET Method is not supported."""
        tg_list = []
        list_all_tg = Taskgroup.objects.all().values()
        list_res = [entry for entry in list_all_tg]
        print(list_res)
        for entry in list_res:
            if entry['author_id']:
                author_id = entry['author_id']
                per_obj = Person.objects.get(id=author_id)
                entry['author_id'] = per_obj.name
            tg_list.append(entry)
        return Response(tg_list, status=HTTP_200_OK)
