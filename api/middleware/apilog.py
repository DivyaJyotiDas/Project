"""This Class is Responsible for Logging All Request and Response in APICall.log File of each Task.

Author:- Divya Jyoti Das
Date:- 01-Oct-2018

"""

import json
import os
from api import apisettings
import logging

request_logger = logging.getLogger('api.logger')


class ApiLog(object):
    """This will Log Request and Response in APICall.log File."""

    def __init__(self, get_response):
        """In Middleware Init."""
        self.get_response = get_response

    def __call__(self, request):
        """Will Function will call repective method ."""
        response = None
        initial_http_body = {}
        initial_http_body = request.body
        if not initial_http_body == b'':
            if hasattr(self, 'process_request'):
                response = self.process_request(request)

        response = response or self.get_response(request)

        if not initial_http_body == b'':
            if hasattr(self, 'process_response'):
                response = self.process_response(request, response)
                return response
        else:
            return response

    def process_request(self, request):
        """Will Process request object."""
        self._initial_http_body = request.body

    def process_response(self, request, response):
        """Will Process Response Object."""
        initial_http_body = ApiLog.http_body(self._initial_http_body)
        context = ApiLog.isContextExist(initial_http_body)
        if context:
            execution_name = ApiLog.isExecutionNameExist(initial_http_body)
            task_name = ApiLog.isTaskNameExist(initial_http_body)
            log_location = apisettings.BASE_DIR + \
                os.sep + \
                "logs" + \
                os.sep + \
                execution_name + \
                os.sep + \
                task_name


            api_log_dump = log_location + os.sep + "APICalls.log"

            f = open(api_log_dump, "a")
            method = "\nMethod:: " + str(request.method) + "\n"
            try:
                path_info = "API:: " + json.dumps(json.loads(request.path_info.decode("utf-8")),
                                                  indent=4) + "\n"
            except:
                path_info = "API:: " + str(request.path_info) + "\n"

            # initial_http_body = "BODY:: " + str(initial_http_body) + "\n"
            response_code = "Response Code:: " + str(response.status_code) + "\n"
            response_content = ApiLog.http_body(response.content)

            if type(response_content) is dict:
                response_content = "Response Content:: " + json.dumps(response_content, indent=4) + "\n"
            else:
                response_content = "No Response Content Found."
                if response.content.decode("utf-8") == "200":
                    response_content = "Response Content:: No Response Content Found" + "\n"
                else:
                    response_content = "Response Content:: "+response.content.decode("utf-8") + "\n"

            f.write("=====================================================\n")
            f.write(method)
            f.write(path_info)
            # f.write(initial_http_body)

            try:
                f.write("Body :: \n" + json.dumps(initial_http_body, indent=3) + "\n")
            except Exception as e:
                f.write("Body :: " + self._initial_http_body + "\n")

            # f.write(json.dumps(json.loads(initial_http_body), indent=4))
            f.write(response_code)
            f.write(response_content)
            f.write("=====================================================\n")
            f.close()

        else:
            pass  # Framework LOg Can be implemnetd here...
        return response

    def http_body(initial_http_body):
        try:
            initial_http_body = initial_http_body.decode('utf-8')
            initial_http_body = json.loads(initial_http_body)
        except Exception as e:
            initial_http_body = {}

        return initial_http_body

    def isContextExist(initial_http_body):
        try:
            if initial_http_body.get('context'):
                return True
            else:
                return False
        except Exception as e:
            return False

    def isExecutionNameExist(initial_http_body):
        if initial_http_body.get('context').get('executionName'):
            return initial_http_body.get('context').get('executionName')
        else:
            return False

    def isTaskNameExist(initial_http_body):
        if initial_http_body.get('context').get('taskName'):
            return initial_http_body.get('context').get('taskName')
        else:
            return False
