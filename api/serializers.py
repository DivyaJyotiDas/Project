"""This is serializers which will serialize models data to json format.

1. PersonSerializers
2. TaskSerializers
3. TaskgroupSerializers
4. TaskgroupTaskSerializers
5. TaskgroupexecutionSerializers
6. TaskExecutionResultSerializers
"""

from rest_framework import serializers
from api.models import Person, \
                        Tafv2Task, \
                        Taskgroup, \
                        TaskgroupTask, \
                        TaskExecutionResult, \
                        Taskgroupexecution


class PersonSerializers(serializers.ModelSerializer):
    """PersonSerializers for serializing Person Model."""

    class Meta:
        """Meta for PersonSerializers."""

        model = Person
        fields = ('id', 'name', 'email_address')


class Tafv2TaskSerializers(serializers.ModelSerializer):
    """TaskSerializers for serializing Person Model."""

    class Meta:
         """Meta for PersonSerializers."""

         model = Tafv2Task
         fields = (
                   'id',
                   'summary',
                   'script',
                   'steps',
                   'expected_results',
                   'author',
                   'summary',
                   'last_modified_by',
                   'added_at',
                   'last_updated_at',
                   'max_execution_time_in_minutes',
                   'tag_name'
                  )


class TaskgroupSerializers(serializers.ModelSerializer):
    """TaskgroupSerializers for serializing Person Model."""

    class Meta:
        """Meta for PersonSerializers."""

        model = Taskgroup
        fields = (
            'id',
            'name'
        )


class TaskgroupTaskSerializers(serializers.ModelSerializer):
    """TaskgroupTaskSerializers for serializing Person Model."""

    class Meta:
        """Meta for PersonSerializers."""

        model = TaskgroupTask
        fields = ('taskgroup', 'task_id',)


class TaskgroupexecutionSerializers(serializers.ModelSerializer):
    """TaskgroupexecutionSerializers for serializing Person Model."""

    class Meta:
        """Meta for PersonSerializers."""

        model = Taskgroupexecution
        fields = (
                    'id',
                    'name',
                    'taskgroup_id',
                    'start_time',
                    'end_time'
                )


class TaskExecutionResultSerializers(serializers.ModelSerializer):
    """TaskExecutionResultSerializers for serializing Person Model."""

    class Meta:
        """Meta for PersonSerializers."""

        model = TaskExecutionResult
        fields = (
                    'execution_id',
                    'task_id',
                    'result',
                    'start_time',
                    'end_time'
                )
