"""This Class is Responsible for Periodic Updation of DB.

Author:- Divya Jyoti Das(divya.das@cumulus-systems.com)
"""
import os
import json

from api.apisettings import BASE_DIR
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import (
                                    HTTP_200_OK,
                                    HTTP_400_BAD_REQUEST
                                )
from api.models import Person, Tafv2Task
from datetime import datetime, timedelta
from api import apisettings


class TaskUpdateView(APIView):
    """This class is for updation of tasks in db.

    Logic:- It will periodic check for tasks in BASE_DIR Location.
    once found will update DB.
    But it wont rewrite DB.

    """

    def get(self, request):
        """GET Verb is not supported so just returning 400 status code."""
        Response(
                    context={
                                "status": "GET not supported"
                            },
                    status=HTTP_400_BAD_REQUEST
                )

    def post(self, request):
        """POST method will update the DB on regular interval."""
        task_path = BASE_DIR+os.sep+"api"+os.sep+"tasks"
        file_name = os.listdir(task_path)
        logger = Log.get_logger(__name__)
        files = []
        addedAt = json.dumps((datetime.now() + timedelta(minutes=apisettings.IST)).strftime('%a %b %d %Y %X')).replace('"', '')
        lastUpdatedAt = json.dumps((datetime.now() + timedelta(minutes=apisettings.IST)).strftime('%a %b %d %Y %X')).replace('"', '')
        for task in file_name:
            try:
                task_name = task_path+os.sep+task+os.sep+task+".info"
                file1 = open(task_name, "r")
                file = json.loads(file1.read())
            except Exception as FileNotFoundError:
                logger.exception("Exception in Task:- {}".format(task_name))
                logger.exception(FileNotFoundError)
                return  Response(
                    {
                        "TaskName": task,
                        "Location": task_name
                    },
                    status=HTTP_400_BAD_REQUEST
                )

            try:
                summary = file['summary']
                script = file['script']
                expectedResults = file["expectedResults"]
                authorId = file["authorId"]
                tagName = file["tagName"]
                steps = file['steps']
                maxExecutionTimeInMinutes = file["maxExecutionTimeInMinutes"]

            except Exception as ke:
                files.append(task)
                write_file = open(task_name, "w")
                task_template = {
                        "summary": task,
                        "script": task,
                        "steps": "mandatory.",
                        "expectedResults": "mandatory",
                        "authorId": "Divya Das",
                        "maxExecutionTimeInMinutes": "120",
                        "tagName": "mandatory"
                    }
                write_file.write(json.dumps(task_template, indent=2))

            try:
                task_obj = Tafv2Task.objects.filter(script=task).count()
                per_obj = Person.objects.get(name=authorId)
                if not task_obj:
                    task_obj = Tafv2Task(
                        summary=summary,
                        script=script,
                        expected_results=expectedResults,
                        author_id=per_obj.id,
                        steps=steps,
                        last_modified_by=authorId,
                        added_at=addedAt,
                        last_updated_at=lastUpdatedAt,
                        max_execution_time_in_minutes=maxExecutionTimeInMinutes,
                        tag_name=tagName

                    )
                    task_obj.save()
                else:
                    lastUpdatedAt = json.dumps(
                        (datetime.now() + timedelta(minutes=apisettings.IST)).strftime('%a %b %d %Y %X')).replace('"', '')
                    task_obj = Tafv2Task.objects.get(script=task)
                    task_obj.summary = summary
                    task_obj.expected_results = expectedResults
                    task_obj.author_id = per_obj.id
                    task_obj.steps = steps
                    task_obj.max_execution_time_in_minutes = maxExecutionTimeInMinutes
                    task_obj.last_updated_at = lastUpdatedAt
                    task_obj.tag_name = tagName
                    task_obj.save(
                        update_fields=[
                            'summary',
                            'expected_results',
                            'author_id',
                            'steps',
                            'last_updated_at',
                            'max_execution_time_in_minutes',
                            'tag_name'
                        ])

            except Exception as Tafv2TaskExcetion:
                logger.exception("Exception:- {}".format(Tafv2TaskExcetion))
                return Response(
                    {
                        "TaskName": task,
                        "Location": task_name
                    },
                    status=HTTP_400_BAD_REQUEST
                )

        return Response(
            {
                "fileNeedToBeModified": files,
                "summary": "mandatory",
                "script": "mandatory",
                "expectedResults": "mandatory",
                "authorId": "mandatory",
                "maxExecutionTimeInMinutes": "mandatory"
            }
        )
