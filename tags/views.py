from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, permission_required

from .models import Tag, TagGroup

@permission_required('tags.view_tag_control_panel')
def edit(request, group_id=0):
    group_id = int(group_id)

    context = {
        'groups': TagGroup.objects.all()
    }

    if group_id > 0:
        try:
            context['group'] = TagGroup.objects.get(pk=group_id)
            context['tags'] = context['group'].tag_set.all().order_by('label')
        except TagGroup.DoesNotExist:
            return HttpResponseRedirect('/tags/edit/')

    return render(request, 'tags/edit.html', context)

@permission_required('tags.add_tag')
def new(request, group_id):
    group_id = int(group_id)

    try:
        group = TagGroup.objects.get(pk=group_id)
    except (TagGroup.DoesNotExist):
        return JsonResponse({
            'success': False,
            'error': 'Unable to find category'
        })

    if 'tag' in request.POST and request.POST['tag']:
        label = request.POST['tag'].strip().lower()
        try:
            tag = Tag.objects.create(label=label, group=group)
            return JsonResponse({
                'success': True,
                'pk': tag.id,
            })
        except IntegrityError:
            return JsonResponse({
                'success': False,
                'error': 'Tag already exists',
            })
    else:
        return JsonResponse({
            'success': False,
            'error': 'Tag cannot be empty'
        })

@permission_required('tags.delete_tag')
def delete(request, tag_id):
    tag_id = int(tag_id)
    try:
        Tag.objects.get(pk=tag_id).delete()
        return JsonResponse({
            'success': True,
        })
    except Tag.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Cannot delete nonexisting tag',
        })