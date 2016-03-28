from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType

def log_change(request, object, title=''):
    if title == '':
        title = object.title
    LogEntry.objects.log_action(
        user_id         = request.user.pk,
        content_type_id = ContentType.objects.get_for_model(object).pk,
        object_id       = object.pk,
        object_repr     = title,
        action_flag     = CHANGE
    )

def log_addition(request, object, title=''):
    if title == '':
        title = object.title
    LogEntry.objects.log_action(
        user_id         = request.user.pk,
        content_type_id = ContentType.objects.get_for_model(object).pk,
        object_id       = object.pk,
        object_repr     = title,
        action_flag     = ADDITION
    )

def log_deletion(request, object, title=''):
    if title == '':
        title = object.title
    LogEntry.objects.log_action(
        user_id         = request.user.pk,
        content_type_id = ContentType.objects.get_for_model(object).pk,
        object_id       = object.pk,
        object_repr     = title,
        action_flag     = DELETION
    )
