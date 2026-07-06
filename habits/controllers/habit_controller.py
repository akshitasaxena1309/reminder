import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from accounts.utils.auth_guard import jwt_required
from habits.dto.habit_dto import CreateHabitDTO, UpdateHabitDTO, ValidationError
from habits.services.habit_service import HabitService, HabitError

from django.conf import settings
from habits.services.reminder_service import ReminderService
service = HabitService()


def _parse_body(request) -> dict:
    try:
        return json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return {}


# ---------- Pages ----------

def add_reminder_page(request):
    return render(request, "add_reminder.html")


# ---------- API ----------

@csrf_exempt
@jwt_required
@require_http_methods(["GET", "POST"])
def habits_collection(request):
    if request.method == "POST":
        try:
            dto = CreateHabitDTO(_parse_body(request))
            habit = service.create_habit(request.user_id, dto)
            return JsonResponse(habit, status=201)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

    habits = service.list_habits(request.user_id)
    return JsonResponse({"habits": habits}, status=200)


@csrf_exempt
@jwt_required
@require_http_methods(["GET", "PATCH", "DELETE"])
def habit_detail(request, habit_id):
    try:
        if request.method == "DELETE":
            service.delete_habit(habit_id, request.user_id)
            return JsonResponse({"message": "Habit deleted."}, status=200)

        if request.method == "PATCH":
            dto = UpdateHabitDTO(_parse_body(request))
            habit = service.update_habit(habit_id, request.user_id, dto)
            return JsonResponse(habit, status=200)

        habit = service.get_habit(habit_id, request.user_id)
        return JsonResponse(habit, status=200)

    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except HabitError as e:
        return JsonResponse({"error": str(e)}, status=404)


def trigger_reminders(request):
    secret = request.GET.get("secret")
    if secret != settings.CRON_SECRET:
        return JsonResponse({"error": "Forbidden"}, status=403)

    result = ReminderService().run_reminders()
    return JsonResponse({"status": "ok", "result": result})