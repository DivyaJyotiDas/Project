"""Validating Body from api.

validation
validation

"""


class TaskGroupExecutionValidation():
    """Validating TaskGroup Body Here with parametrs.

    AuthenticationMiddleware
    AuthenticationMiddleware
    """

    def __init__(self, data, files):
        """Constructor Initializing data and files."""
        self.data = data
        self.files = files

    def is_valid(self):
        """Checking logioc for valid input."""
        key = []
        if not bool(self.data):
            return False
        else:
            for keys in self.data:
                key.append(keys)
                if keys == "":
                    return False
                if len(key) > 2:
                    return True
                if keys != "taskGroupName" and keys != "tasks" and keys != "setup" and keys != "tafServerURL" and keys != "repo" and keys != "browser" and keys != "notify":
                    return True
                if keys == "taskGroupName":
                    if self.data[keys] == "":
                        return False
                    if len(self.data[keys]) > 1:
                        return False
                    return True
                if keys == "tasks":
                    return True
            return True
