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


from api.models import Person
from api.models import Tafv2Task
import  json




class TestCasesTrackView(APIView):
    """This class implemnets ExecutionInfo."""

    def get(self, request):
        tc_obj = Tafv2Task.objects.all()

        data1 = []

        for obj in tc_obj:
            data = {}
            data['id'] = obj.id
            owner = Person.objects.get(id=obj.author_id)
            data['scripts'] = obj.script
            data['owner'] = owner.name
            data['summary'] = obj.summary
            data['steps'] = obj.steps
            data['expectedResults'] = obj.expected_results
            data['submissionTime'] = obj.added_at
            data['tags'] = obj.tag_name
            data['lastEditedSubmissionTime'] = obj.last_updated_at
            data['lastEditedAuthor'] = obj.last_modified_by
            data['maxExecutionTimeInMinutes'] = obj.max_execution_time_in_minutes
            data1.append(data)
        return Response(data1, status=HTTP_200_OK)

    def post(self, request):
        test_case_context = request.POST
        author = test_case_context.get('tc_author', None)
        summary = test_case_context.get('tc_id', None)
        steps = test_case_context.get('tc_name', None)
        expected_results = test_case_context.get('tc_comment', None)
        submission = test_case_context.get('tc_submission', None)
        tag_name = test_case_context.get('tag_name', None)
        max_exec_time_in_min = test_case_context.get("max_exec_time_in_min", None)
        print(summary, steps, expected_results, author, submission, max_exec_time_in_min)

        try:
            owner = Person.objects.get(name=author)
            owner_id = Person.objects.get(id=owner.id)
        except Exception as e:
            pass



        tc_obj = Tafv2Task(
            summary=summary,
            script=None,
            steps=steps,
            expected_results=expected_results,
            author_id=owner.id,
            last_modified_by=owner_id.name,
            added_at=submission,
            last_updated_at=submission,
            max_execution_time_in_minutes=max_exec_time_in_min,
            tag_name=tag_name
        )
        tc_obj.save()

        return Response(status=HTTP_200_OK)

    def put(self, request):
        edit_tc_context = request.POST
        author = edit_tc_context.get('tc_author', None)
        tc_id = edit_tc_context.get('tc_id', None)
        summary = edit_tc_context.get('summary', None)
        steps = edit_tc_context.get('tc_name', None)
        expectedResults = edit_tc_context.get('tc_comment', None)
        submission = edit_tc_context.get("tc_submission", None)
        tag_name = edit_tc_context.get("tag_name", None)
        last_edited_submission_time = edit_tc_context.get("last_edited_submission_time", None)
        max_execution_time_in_minutes = edit_tc_context.get("max_execution_time_in_minutes", None)
        print(tc_id, author, summary, steps, expectedResults, submission, tag_name, max_execution_time_in_minutes)

        try:
            owner = Person.objects.get(name=author)
        except Exception as e:
            print(e)

        task_edit_obj = Tafv2Task.objects.get(id= tc_id)
        task_edit_obj.last_modified_by= owner.name
        task_edit_obj.last_updated_at = last_edited_submission_time
        task_edit_obj.summary = summary
        task_edit_obj.steps = steps
        task_edit_obj.expected_results = expectedResults
        task_edit_obj.tag_name = tag_name
        task_edit_obj.max_execution_time_in_minutes = max_execution_time_in_minutes
        task_edit_obj.save()
        print(task_edit_obj.id, task_edit_obj.summary)


        return  Response(status=HTTP_200_OK)
