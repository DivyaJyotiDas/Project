from api import apisettings
import requests
import  json

class tafv2Log(Exception):
    @staticmethod
    def dumpLog(mode, msg, context):
        try:
            headers = apisettings.HEADERS_JSON
            log_url = context['TAFServerURL'] + apisettings.LOG_API
            logInputJSON = {}
            logInputJSON['context'] = context
            logInputJSON['mode'] = mode
            logInputJSON['message'] = msg
            requests.post(
                            url=log_url,
                            data=json.dumps(logInputJSON),
                            headers=headers
                            )
        except LogError as le:
            raise le

class LogError(Exception):
    @staticmethod
    def inputException():
        return "Log API input Error."

class stepResultException(Exception):
    pass

class taskResultException(Exception):
    pass

class ipv6Exception(Exception):
    pass

class ipv4Exception(Exception):
    pass