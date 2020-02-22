"""This is admin Page."""

from django.contrib import admin

from api.models import Person, \
                        TaskExecutionResult, \
                        Taskgroup, \
                        Taskgroupexecution, \
                        TaskgroupTask

# Register your models here.
admin.site.register(Person)
admin.site.register(TaskExecutionResult)
admin.site.register(Taskgroup)
admin.site.register(Taskgroupexecution)
admin.site.register(TaskgroupTask)
