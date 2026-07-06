import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ValidationError(Exception):
    pass


class RegisterDTO:
    """Validates and normalizes registration input before it reaches the service layer."""

    def __init__(self, data: dict):
        self.name = (data.get("name") or "").strip()
        self.email = (data.get("email") or "").strip().lower()
        self.password = data.get("password") or ""
        self._validate()

    def _validate(self):
        if not self.name or len(self.name) < 2:
            raise ValidationError("Name must be at least 2 characters.")
        if not EMAIL_RE.match(self.email):
            raise ValidationError("Invalid email format.")
        if len(self.password) < 6:
            raise ValidationError("Password must be at least 6 characters.")


class LoginDTO:
    """Validates login input."""

    def __init__(self, data: dict):
        self.email = (data.get("email") or "").strip().lower()
        self.password = data.get("password") or ""
        self._validate()

    def _validate(self):
        if not self.email or not EMAIL_RE.match(self.email):
            raise ValidationError("Valid email is required.")
        if not self.password:
            raise ValidationError("Password is required.")