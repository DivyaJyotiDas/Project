# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ApiTask(models.Model):
    id = models.ForeignKey('Person', models.DO_NOTHING, db_column='id', primary_key=True)
    name = models.CharField(unique=True, max_length=200, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    owner_id = models.SmallIntegerField(blank=True, null=True)
    max_execution_time_in_minutes = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'api_task'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Person(models.Model):
    name = models.CharField(max_length=200)
    email_address = models.CharField(max_length=200)

    class Meta:
        managed = True
        db_table = 'person'


class Tafv2Task(models.Model):
    summary = models.TextField(blank=True, null=True)
    script = models.CharField(unique=True, max_length=200, blank=True, null=True)
    steps = models.TextField(blank=True, null=True)
    expected_results = models.TextField(blank=True, null=True)
    author = models.ForeignKey(Person, models.DO_NOTHING, blank=True, null=True)
    last_modified_by = models.CharField(max_length=500, blank=True, null=True)
    added_at = models.CharField(max_length=500, blank=True, null=True)
    last_updated_at = models.CharField(max_length=500, blank=True, null=True)
    max_execution_time_in_minutes = models.SmallIntegerField(blank=True, null=True)
    tag_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tafv2_task'


class Tags(models.Model):
    name = models.CharField(unique=True, max_length=200, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tags'


class TaskBkp(models.Model):
    display_name = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(unique=True, max_length=200, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    owner = models.ForeignKey(Person, models.DO_NOTHING, blank=True, null=True)
    max_execution_time_in_minutes = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'task_bkp'


class TaskExecutionResult(models.Model):
    execution_id = models.BigIntegerField(blank=True, null=True)
    task_id = models.BigIntegerField(blank=True, null=True)
    result = models.SmallIntegerField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'task_execution_result'


class Taskgroup(models.Model):
    name = models.CharField(unique=True, max_length=300, blank=True, null=True)
    author = models.ForeignKey(Person, models.DO_NOTHING, blank=True, null=True)
    last_modified_by = models.CharField(max_length=500, blank=True, null=True)
    added_at = models.CharField(max_length=500, blank=True, null=True)
    last_updated_at = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'taskgroup'


class TaskgroupTask(models.Model):
    taskgroup = models.ForeignKey(Taskgroup, models.DO_NOTHING, blank=True, null=True)
    task_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'taskgroup_task'


class Taskgroupexecution(models.Model):
    name = models.CharField(unique=True, max_length=200, blank=True, null=True)
    taskgroup = models.ForeignKey(Taskgroup, models.DO_NOTHING, blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    alias_name = models.CharField(max_length=500, blank=True, null=True)
    mode = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'taskgroupexecution'


class TestcaseBkp(models.Model):
    author = models.ForeignKey(Person, models.DO_NOTHING, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    steps = models.TextField(blank=True, null=True)
    expected_results = models.TextField(blank=True, null=True)
    submission_time = models.CharField(max_length=500, blank=True, null=True)
    tag_name = models.TextField(blank=True, null=True)
    last_edited_submission_time = models.CharField(max_length=500, blank=True, null=True)
    modified_owner = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'testcase_bkp'
