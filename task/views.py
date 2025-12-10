
import json
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.utils.dateparse import parse_datetime

from .models import Task


def json_error(message, status=400):
    return JsonResponse({"detail": message}, status=status)


@csrf_exempt
def tasks_list_create(request):
    if request.method == "GET":
        qs = Task.objects.all()

        # Filtering
        status_param = request.GET.get('status')
        if status_param:
            qs = qs.filter(status=status_param)

        priority_param = request.GET.get('priority')
        if priority_param:
            qs = qs.filter(priority=priority_param)

        ordering = request.GET.get('ordering')
        if ordering in ['created_at', '-created_at']:
            qs = qs.order_by(ordering)
        else:
            qs = qs.order_by('-created_at')

        data = [t.to_dict() for t in qs]
        return JsonResponse(data, safe=False, status=200)

    elif request.method == "POST":
        try:
            payload = json.loads(request.body.decode('utf-8') or "{}")
        except json.JSONDecodeError:
            return json_error("Invalid JSON.", status=400)

        title = payload.get('title')
        if not title or not str(title).strip():
            return json_error("Title is required and cannot be empty.", status=400)

        description = payload.get('description', '')
        priority = payload.get('priority', Task.PriorityChoices.MEDIUM)
        status_val = payload.get('status', Task.StatusChoices.PENDING)

        # Validate choices
        if priority not in dict(Task.PriorityChoices.choices).keys():
            return json_error(f"Invalid priority. Allowed: {list(dict(Task.PriorityChoices.choices).keys())}", status=400)
        if status_val not in dict(Task.StatusChoices.choices).keys():
            return json_error(f"Invalid status. Allowed: {list(dict(Task.StatusChoices.choices).keys())}", status=400)

        task = Task.objects.create(
            title=title.strip(),
            description=description,
            priority=priority,
            status=status_val,
        )
        return JsonResponse(task.to_dict(), status=201)

    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@csrf_exempt
def task_detail(request, pk):
   
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return json_error("Task not found.", status=404)

    if request.method == "GET":
        return JsonResponse(task.to_dict(), status=200)

    elif request.method in ("PUT", "PATCH"):
        try:
            payload = json.loads(request.body.decode('utf-8') or "{}")
        except json.JSONDecodeError:
            return json_error("Invalid JSON.", status=400)

        # For PUT, require title (full update). For PATCH, partial allowed.
        if request.method == "PUT":
            title = payload.get('title')
            if not title or not str(title).strip():
                return json_error("Title is required for full update.", status=400)
        else:
            title = payload.get('title', task.title)

        description = payload.get('description', task.description)
        priority = payload.get('priority', task.priority)
        status_val = payload.get('status', task.status)

        # Validate choices
        if priority not in dict(Task.PriorityChoices.choices).keys():
            return json_error(f"Invalid priority. Allowed: {list(dict(Task.PriorityChoices.choices).keys())}", status=400)
        if status_val not in dict(Task.StatusChoices.choices).keys():
            return json_error(f"Invalid status. Allowed: {list(dict(Task.StatusChoices.choices).keys())}", status=400)

        # Apply updates
        task.title = str(title).strip()
        task.description = description
        task.priority = priority
        task.status = status_val
        task.save()
        return JsonResponse(task.to_dict(), status=200)

    elif request.method == "DELETE":
        task.delete()
        
        return JsonResponse({"detail": "Task deleted successfully."}, status=204)

    else:
        return HttpResponseNotAllowed(['GET', 'PUT', 'PATCH', 'DELETE'])


def tasks_summary(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(['GET'])

    summary_qs = Task.objects.values('status').annotate(count=Count('id'))
    data = {item['status']: item['count'] for item in summary_qs}

    # Ensure all statuses present
    for status_choice in Task.StatusChoices.values:
        data.setdefault(status_choice, 0)

    return JsonResponse(data, status=200)
