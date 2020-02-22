"""This is the implementation class od Result API.

Author:- Divya Jyoti Das(divya.das@cumulus-systems.com)
API:- /api/task/result
GET:- Not Supported
POST:- Supported.

"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
                    HTTP_400_BAD_REQUEST,
                    HTTP_200_OK
                        )
from api.models import TaskExecutionResult
from api import apisettings


class ResultView(APIView):
    """This Class implemnets POST method for Result."""

    def get(self, request):
        """GET is not supported."""
        return Response(status=HTTP_400_BAD_REQUEST)

    def post(self, request):
        """Implemnetation of REsult API in POST."""
        result = None
        print("RESULT API: ", request.data)
        task_exec_update = TaskExecutionResult.objects.get(
                                id=request.data['context']['taskExecutionID']
                                )
        try:
            if request.data['result'].lower() == "pass":
                result = apisettings.PASS
            if request.data['result'].lower() == "fail":
                result = apisettings.FAIL
            if request.data['result'].lower() == "abort":
                result = apisettings.ABORT

            task_exec_update.result = result
            task_exec_update.save(update_fields=['result'])
            Log.summary_task_result(context=request.data.get("context"), result=request.data['result'])
            return Response(status=HTTP_200_OK)
        except Exception as e:
            logger = Log.get_logger(__name__)
            logger.exception(e)
            return Response(status=HTTP_400_BAD_REQUEST)
