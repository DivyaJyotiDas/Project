import random
import string

from rest_framework.response import Response
from api.lib.projects.HDCA.zip.zipUpgradeWrapper import ZipUpgradeWrapper
from api.models import *
from api.serializers import *
from rest_framework.views import APIView
from api.lib.common import Installer, configure, Login
from api.lib.log.log import Log, LOG_FOLDER_LOCATION
from api.lib.common.RemoteCommand import RemoteCommand
from api.lib.jetty import jetty
from api.lib.file.RemoteCommand import RemoteTransfer
from rest_framework import status, viewsets
from api.lib.projects.HDCA.License.ProbeLicenseDetails import GetProbeLicDetails
from api.lib.projects.HDCA.License.ServerLicenseDetails import GetServerLicDetails
from api.lib.projects.HDCA.Login.ProbeAdd import HESP
from api.lib.projects.HDCA.zip import zipUpgradeWrapper
# from api.apisettings import LOG_FOLDER_LOCATION
from datetime import datetime
from django.db.models import Model
from django.core import serializers
from jsondiff import diff
import json, os
import logging
from api.lib.projects.HDCA.SystemUpgrade.systemUpgrade import SystemUpgrade


class LogInfoView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        list_of_files = os.listdir(LOG_FOLDER_LOCATION)
        return Response("hello logs.")


class TaskGroupCreateView(APIView):
    """
        This api creates TaskGroup.\n
        HTTP Method     :        POST\n
        URL             :        /api/taskGroup/create\n
        Request Body    :        {\n
                                   name    : â€œâ€�,  //name of the taskGroup to be created\n
                                   tasks   : [â€œâ€�],//listoftasks.\n
                                 }\n
        Response        :        {\n
                                 }\n
        Error Codes     :        â€¢ 200(OK)\n
                                 â€¢ 400(Bad Request) \n
        Notes           :        â€¢ The tasksinataskGroupgetexecutedinthegivenorder(given in â€œtasksâ€� input here) during execution of the taskGroup.\n
    """

    def get(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = TaskGroupCreateSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                status=status.HTTP_200_OK)  # if you want to send data as response use serializer.data as args
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskCreateView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = TaskSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskInfoView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        task_info = TaskModel.objects.filter(name=request.data['name']).values()
        print(task_info)
        return Response(task_info)


class TaskGroupInfoView(APIView):
    def get(self, request):
        taskgroup_create = TaskGroupCreateModel.objects.all()
        serializer = TaskGroupCreateSerializers(taskgroup_create, many=True)
        return Response(serializer.data)


class TaskGroupExecuteView(APIView):
    """\n
        HTTP Method    :     POST\n
	URL            :     /api/taskGroup/execute\n
	Request Body   :
				{
					taskGroup:â€œâ€� //name ofthetaskGrouptobeexecuted
				}
	Response       :    	{
					executionID:â€œâ€� //dynamically auto-Â­â€�generated ID of this execution of the taskGroup
				}
Error Codes
				â€¢ 200(OK)
				â€¢ 400(Bad Request)
Notes				â€¢ Client needs to make subsequent API call to fetch status progress of the execution by passing the returned â€œexecutionIDâ€�
    """

    def get(self, request):
        return Response({'test': 'It worked.'})

    def post(self, request):
        data = request.data
        print(data)
        if data:
            new_entry_response = ExecTasks.executeTasksList(data)
            executionID = TaskGroupExecutionModel.objects.all()
            serializer = TaskGroupExecutionSerializers(executionID, many=True)
            return Response({'executionID': serializer.data[TaskGroupExecutionModel.objects.count() - 1]['executionID'],
                             'Name': serializer.data[TaskGroupExecutionModel.objects.count() - 1]['name']})
        else:
            return Response({'Result': 'Json Not Received.'})


class TaskGroupExecutionInfoView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        req = request.data
        tg_info = TaskGroupExecutionModel.objects.filter(executionID=req['executionID']).values()
        tasks_info = TaskExecutionModel.objects.filter(taskgroupRelation=req['executionID']).values()
        tg_serializer = TaskGroupExecutionSerializers(tg_info, many=True)
        tasks_serializer = TaskExecutionSerializers(tasks_info, many=True)
        tg_info_list = list(tg_info)
        tasks_info_list = list(tasks_info)
        tg_info_list.insert(len(tg_info_list), tasks_info_list)
        return Response(tg_info_list)


class CommonConfigureSetupView(APIView):

    def get(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """
        	HTTP Method                     POST\n
        	URL                                     /api/RPM/install\n
        	Request Body            {
						"host"     : "192.168.100.30",
                				"user"     : "root",
                				"password" : "app.jeos"
                                        }
        	Response                        {
                                                RPMInfo :{}                                         }
        	Error Codes                     â€¢ 200(OK)
                	                        â€¢ 400(BadRequest)
        	Notes           	                â€¢
    """

        try:
            data = request.data

            config = configure.GenericConfig(**data)
            result = config.auto_configure()

            if result:
                data["Result"] = "Pass"
            else:
                data["Result"] = "Fail"
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            Response({"Result": "Fail"})


class HDCALicenseInfoView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            return_json = {}
            request_body = json.loads(request.body.decode('utf-8'))
            logger = Log.get_logger(__name__, request_body.get("context", None), "Get license info")
            logger.info("Get license info API Execution Started ")
            logger.info("Get license info API inputs : %s " % str(request_body))
            from api.lib.projects.HDCA.License.ProbeLicenseDetails import GetProbeLicDetails
            info = GetProbeLicDetails(**request_body)
            returnStatus = info.getProbeLicStatus(**request_body)
            if returnStatus["status"] == True:
                return_json['status'] = "PASS"
                return_json['msg'] = returnStatus["msg"]
                logger.info("Get license info API Execution Completed ..............OK")
                logger.info("Get license info API o/p : %s" % return_json)
                return Response(return_json)
            else:
                return_json['status'] = "FAIL"
                return_json['Valid List'] = returnStatus["msg"]
                logger.info("Get license info API Execution Completed ...............NOT OK")
                logger.info("Get license info API o/p : %s" % return_json)
                return Response(return_json, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception(str(e))



class HDCAServerLicenseInfoView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            return_json = {}
            request_body = json.loads(request.body.decode('utf-8'))
            logger = Log.get_logger(__name__, request_body.get("context", None), "Get Server license info")
            logger.info("Get Server license info API Execution Started ")
            logger.info("Get Server license info API inputs : %s " % str(request_body))
            from api.lib.projects.HDCA.License.ServerLicenseDetails import GetServerLicDetails
            info = GetServerLicDetails(**request_body)
            returnStatus = info.getServerLicStatus(**request_body)
            logger.debug("Return Status : {}".format(returnStatus))
            if returnStatus["status"] == True:
                return_json['status'] = "PASS"
                return_json['msg'] = returnStatus["msg"]
                logger.info("Get license info API Execution Completed ..............OK")
                logger.info("Get license info API o/p : %s" % return_json)
                return Response(return_json)
            else:
                return_json['status'] = "FAIL"
                return_json['Valid List'] = returnStatus["msg"]
                logger.info("Get Server license info API Execution Completed ...............NOT OK")
                logger.info("Get Server license info API o/p : %s" % return_json)
                return Response(return_json, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception(e)
            result = {
                        "status": "FAIL",
                        "message":str(e)
                        }
            return Response(result, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        login_object = Login.CommonLogin(**request.data)
        print(login_object.login())
        return Response(login_object.login())


class InitView(APIView):
    def get(self, request):
        """
           get verb not supported
        """
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """
                HTTP Method                     POST\n
                URL                                     /api/common/init\n
                Request Body            {
                                                "host"     : "192.168.100.30",
                                                "user"     : "root",
                                                "password" : "app.jeos"
                                        }
                Response                        {
                                                RPMInfo :{}                                         }
                Error Codes                     â€¢ 200(OK)
                                                â€¢ 400(BadRequest)
                Notes                                   â€¢
        """
        req = request.data
        if req['db_type'] == 'taskgroup':
            new_entry = TaskGroupExecutionModel(
                name=req['task_name'],
                startTime=str(datetime.now()),
                endTime=None,
                numTasksScheduled=req["scheduled_tasks"],
                numTasksPassed=None,
                numTasksFailed=None,
                numTasksAborted=None
            )
            new_entry.save()
            latest_id = TaskGroupExecutionModel.objects.latest('executionID')
            id = latest_id.executionID
            name = latest_id.name
            return Response({'executionID': id, 'executionName': name})
        else:
            new_entry = TaskExecutionModel(
                taskName=req['taskName'],
                startTime=str(datetime.now()),
                endTime=None,
                result=None,
                taskgroupRelation=TaskGroupExecutionModel.objects.get(executionID=int(req['executionID']))
            )
            new_entry.save()
            task_id = TaskExecutionModel.objects.latest('id')
            id = task_id.id
            return Response({'taskID': id})


class JettyView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        req = request.data
        jetty.start_jetty(req['host'], req['user'], req['password'])
        return Response(status=status.HTTP_200_OK)


class RemoteCommandView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        req = request.data
        rc = RemoteCommand(req['host'], req['user'], req['password'], req['command'])
        print(rc.execute_command())
        return Response(status=status.HTTP_200_OK)


class TransferView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        rt = RemoteTransfer()
        data = request.data
        # status = rt.file_copy(request.data)
        print(status)
        return Response({"status": rt.file_copy(request.data)})


class ResultView(APIView):

    def get(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        context = request.data['context']
        task_object = TaskExecutionModel.objects.get(id=request.data['context']['taskID'])
        logger = Log.get_logger(__name__,context=context)
        try:
            logger.debug("Task Execution ID:: {} ".format(request.data['context']['taskID']))
            logger.debug("Result:: {} ".format(request.data["result"]))
            task_object.result = request.data['result']
            task_object.save()
            Log.summary_task_result(context=context, result=request.data['result'])
        except Exception as e:
            logger.exception(e)
            task_object.result = "abort"
            task_object.save()
        return Response(status=status.HTTP_200_OK)


class EditPrimaryServer(APIView):

    def get(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        return Response(self.common(request, id))

    def post(self, request, id):
        """
        input parameter for kwargs are as follow.
        Note :- all parameter are optional, if not given default value will be taken


        "protocol" : "",
        "hostField" : "",
        "port" : "",
        "user" : "",
        "password" : "",

        "proxy" : {
            "proxyType": "",
            "proxyServer" : "",
            "proxyPort" : "",
            "proxyUser" : "",
            "proxyPassword" : "",
        },
        "realtimeServer" : ""
        """
        return Response(self.common(request, id))

    def common(self, request, id):
        request_body = json.loads(request.body)
        if 'addSecondaryServer' in id:
            from api.lib.projects.HDCA.CommonProbeOperations.reconfiguration.editPrimaryServer import EditPrimaryServer
            edit_primary_server = EditPrimaryServer(request_body['probeIP'], request_body['probeUserName'],
                                                    request_body['probePassword'])
            status = edit_primary_server.edit_primary_server(**request_body)
        return_json = {}
        return_json['status'] = status
        return return_json


class GetSystemStatus(APIView):
    """
    {
        "probeIP"  : "192.168.33.138",
        "probeUserName" : "admin",
        "probePassword" : "Cumulus@1",
        "browser" : "chrome"

    }
    """

    def get(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        return Response(self.common(request))

    def post(self, request):
        return Response(self.common(request))

    def common(self, request):
        request_body = json.loads(request.body)
        from api.lib.projects.HDCA.CommonProbeOperations.getSystemStatus import SystemStatus
        system_status_obj = SystemStatus(request_body['probeIP'], request_body['probeUserName'],
                                         request_body['probePassword'], request_body['browser'])
        status = system_status_obj.get_system_status(**request_body)
        return status


class SetupInfoView(APIView):
    """
    Give the setup detail
    """

    def get(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            log = Log.get_logger(__name__, context=request.data.get("context", None))
            if request.data.get("executionName"):
                log.debug("Reading the setup details")

                with open(os.path.join(LOG_FOLDER_LOCATION, str(request.data["executionName"]), "setup.json"),
                          'r') as outfile:
                    setup = json.load(outfile)

                return Response(setup, status=status.HTTP_200_OK)

            if request.data.get("context"):
                with open(
                        os.path.join(LOG_FOLDER_LOCATION, str(request.data["context"]["executionName"]), "setup.json"),
                        'r') as outfile:
                    setup = json.load(outfile)

                log.debug("Setup Details \n {}".format(json.dumps(setup, indent=4)))

                return Response(setup, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No setup Detail present for current execution ID"},
                                status=status.HTTP_404_NOT_FOUND)
        except FileNotFoundError as e:
            log.exception(e)
            return Response({"message": "No setup Detail present for current execution ID"},
                            status=status.HTTP_404_NOT_FOUND)


class SetupUpdateView(APIView):
    """
    This will update the setup details related to execution task group at run time
    """

    def get(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        log = Log.get_logger(__name__, context=request.data.get("context", None))
        if request.data.get("executionName"):
            log.debug("Reading the setup details")
            with open(os.path.join(LOG_FOLDER_LOCATION, str(request.data["executionName"]), "setup.json"),
                      'r') as outfile:
                setup = json.load(outfile)

        if request.data.get("context"):
            with open(os.path.join(LOG_FOLDER_LOCATION, str(request.data["context"]["executionName"]), "setup.json"),
                      'r') as outfile:
                setup = json.load(outfile)

            log.debug("Setup details before update \n {}".format(json.dumps(setup, indent=4)))
            setup.update(request.data)
            log.debug("Setup details after update \n {}".format(json.dumps(setup, indent=4)))
            with open(os.path.join(LOG_FOLDER_LOCATION, str(request.data["context"]["executionName"]), "setup.json"),
                      'w') as outfile:
                json.dump(setup, outfile, indent=4)

            return Response(setup, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No setup Detail present for current execution ID"},
                            status=status.HTTP_404_NOT_FOUND)


class SetupInitView(APIView):
    def get(self, request):
        """
           get verb not supported
        """
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        log = Log.get_logger(__name__, context=request.data.get("context", None))
        log.debug("Setup Initialzation")
        log.debug("Setup Details are ")
        log.debug(json.dumps(request.data))

        if not os.path.exists(os.path.join(LOG_FOLDER_LOCATION, str(request.data["executionName"]))):
            log.debug("Creating the folder on this location to store the setup.json")
            log.debug(
                "Directory Location : {}".format(os.path.join(LOG_FOLDER_LOCATION, str(request.data["executionName"]))))
            os.makedirs(os.path.join(LOG_FOLDER_LOCATION, str(request.data["executionName"])))

        with open(os.path.join(LOG_FOLDER_LOCATION, str(request.data["executionName"]), "setup.json"), 'w') as outfile:
            json.dump(request.data, outfile, indent=4)

        return Response(request.data, status=status.HTTP_200_OK)


class ZipUpgradeHDCA(APIView):
    """
        This api upgrade zip for HDCA .\n
        HTTP Method     :        POST\n
        URL             :        /api/taskGroup/create\n
        Request Body    :        {\n
                                   ip    : â€œâ€�,  //setup ip \n
                                   username   : "",//GUI username.\n
                                   password   : "",//GUI password
                                   zip_build_sequence :["",""]\n
                                 }\n
                                 Proper input for zip_build_sequence are as follow. only one entry should be given \n
                                 1. hdca-probe-8.1.1-17060913 or hdca-probe-8.1.1-17060913.zip or hdca-probe-8.1.1-17060913.zip.hash\n
                                    It search the file on running server on this location data/zip/HDCA/release\n
                                 2. ftp://192.168.20.138/hdca_probe_master/ (mainly used for nightly build) or ftp://<ip>/<location>/hdca-probe-9.0.0-00_18042707.zip.hash \n
                                    or ftp://<ip>/<location>/hdca-probe-9.0.0-00_18042707.zip.hash \n
                                3. https//<link>/hdca-probe-9.0.0-00_18042707.zip.hash or https//<link>/hdca-probe-9.0.0-00_18042707.zip \n
                                   or https//<link>/hdca-probe-9.0.0-00_18042707\n

        Response        :        {\n
                                 }\n
        Error Codes     :        â€¢ 200(OK)\n
                                 â€¢ 400(Bad Request) \n
        Notes           :        â€¢ Extra information error_msg give for debugging purpose.\n
    """

    def get(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            print("Calling the request with url")
            print(request.url)
        except Exception as e:
            print("Exception occur while calling the request url")

        try:
            print("Calling with absolute url")
            print(request.build_absolute_uri)
        except Exception as e:
            print("Exception Occur while calling the url")

        zip_upgrade_obj = ZipUpgradeWrapper()
        try:
            output = zip_upgrade_obj.zip_upgrade(**request.data)
            if isinstance(output, tuple):
                return Response({"error_msg": output[1]}, status=status.HTTP_400_BAD_REQUEST)
            elif output:
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
