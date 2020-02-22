from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from django.template import loader
from django.shortcuts import render
from ldap3 import Server, Connection, ALL, SUBTREE
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
import  ast, json
from api import apisettings
from functools import wraps
from api.models import Person
from api.serializers import PersonSerializers

#TODO:- Implement a login_required decorator so that code duplication can be avoided.
def login_required(request):
    @wraps(request)
    def wrap(request):
        if not request.session.get('displayName', False):
            return render(
                request,
                'index.html')
    return wrap


def LoginView(request):
    if request.session.get('displayName', False):
        context = {
            'session': request.session
        }
        return render(request, 'header.html', {'context': context})
    else:
        template = loader.get_template('index.html')
        context = {
            'name': 'index',
        }
        return HttpResponse(template.render(context, request))


def HomeView(request):
    total_entries = 0
    if request.POST:
        request_body = request.POST
        username = request_body.get('email', False)
        password = request_body.get('passwd', False)
        ldap_conn = Connection(apisettings.LDAP_SERVER, "corp\\" + username, password)
        try:
            # ldap_conn.open()
            # if ldap_conn.bind():
            #     ldap_conn.search(search_base="CN=Users,DC=corp,DC=cumulus", search_filter='(mail=*)', search_scope=SUBTREE,
            #                      attributes='*')
            #     total_entries += len(ldap_conn.response)
            #     for entry in ldap_conn.response:
            #         if entry['attributes']['sAMAccountName'] == username:
            #             request.session['displayName'] = entry['attributes']['displayName']
            #             request.session['mailID'] = entry['attributes']['mail']
            #             try:
            #                 owner = Person.objects.get(name=entry['attributes']['displayName'])
            #             except Exception as e:
            #                 per_obj = Person(
            #                     name=entry['attributes']['displayName'],
            #                     email_address=entry['attributes']['mail']
            #                 )
            #                 per_obj.save()

                context = {
                    'session': request.session
                }
                return render(request, 'header.html', {'context': context})
        except Exception as e:
            print(e)
        msg = "<html><body><script>alert(\"404 ERROR... Pls Enter Correct Creds.\");</script></body></html>"
        return HttpResponse(msg)
    else:
        if request.session.get('displayName', False):
            context = {
                'session': request.session
            }
            return render(
                request,
                'header.html',
                {'context': context}
            )
        else:
            return render(
                request,
                'index.html')


def LogoutView(request):
    if request.session.get('displayName', False):
        del request.session['displayName']
        template = loader.get_template('index.html')
        context = {
            'name': 'index',
        }
        return HttpResponse(template.render(context, request))
    else:
        return render(
            request,
            'index.html')


def TasksView(request):
    if request.session.get('displayName', False):
        context = {
            'session': request.session
        }
        return render(
            request,
            'html/tasks_addition.html',
            {'context': context}
        )
    else:
        return render(
            request,
            'html/tasks_addition.html')


def TaskgroupView(request):
    if request.session.get('displayName', False):
        context = {
            'session': request.session
        }
        return render(
            request,
            'html/taskgroup.html',
            {'context': context}
        )
    else:
        return render(
            request,
            'html/taskgroup.html')


