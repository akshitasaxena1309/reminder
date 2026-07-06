import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from accounts.dto.auth_dto import RegisterDTO, LoginDTO, ValidationError
from accounts.services.auth_service import AuthService, AuthError
from accounts.utils.jwt_handler import decode_token

service = AuthService()


def _parse_body(request) -> dict:
    try:
        return json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return {}


# ---------- Page renderers ----------

def login_page(request):
    return render(request, "login.html")


def register_page(request):
    return render(request, "register.html")


def dashboard_page(request):
    return render(request, "dashboard.html")


# ---------- API endpoints ----------

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    try:
        dto = RegisterDTO(_parse_body(request))
        result = service.register(dto)
        return JsonResponse(result, status=201)
    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except AuthError as e:
        return JsonResponse({"error": str(e)}, status=409)


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    try:
        dto = LoginDTO(_parse_body(request))
        result = service.login(dto)
        return JsonResponse(result, status=200)
    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except AuthError as e:
        return JsonResponse({"error": str(e)}, status=401)


@csrf_exempt
@require_http_methods(["GET"])
def me(request):
    """Protected endpoint — requires 'Authorization: Bearer <token>' header."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return JsonResponse({"error": "Missing or malformed token"}, status=401)

    token = auth_header.split(" ", 1)[1]
    payload = decode_token(token)
    if not payload:
        return JsonResponse({"error": "Invalid or expired token"}, status=401)

    try:
        user = service.get_profile(payload["sub"])
        return JsonResponse({"user": user}, status=200)
    except AuthError as e:
        return JsonResponse({"error": str(e)}, status=404)