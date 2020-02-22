"""This module is for validation of inputs from create API.

API:- api/taskGroup/create

"""
from api.validation.taskgroup_execution_validation import (
                                                TaskGroupExecutionValidation
                                                            )


class TaskGroupCreateValidation(TaskGroupExecutionValidation):
    """Validating the inputs."""
