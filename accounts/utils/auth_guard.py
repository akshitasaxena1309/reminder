from functools import wraps
from django.http import JsonResponse
from accounts.utils.jwt_handler import decode_token


def jwt_required(view_func):
    """
    Decorator for API views. Validates the Bearer token and attaches
    request.user_id / request.user_email for the view to use.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return JsonResponse({"error": "Missing or malformed token"}, status=401)

        token = auth_header.split(" ", 1)[1]
        payload = decode_token(token)
        if not payload:
            return JsonResponse({"error": "Invalid or expired token"}, status=401)

        request.user_id = payload["sub"]
        request.user_email = payload.get("email")
        return view_func(request, *args, **kwargs)

    return wrapper