"""This Class Responsible for returning executionInfo.

Author:- Divya Jyoti Das(divya.das@cumulus-systems.com)
"""

from django.http import HttpResponse
from django.template import loader


def DashboardView(request):
    """This class implemnets ExecutionInfo."""
    template = loader.get_template('dashboard.html')
    context = {
        'name': 'dashboard',
    }
    return HttpResponse(template.render(context, request))


