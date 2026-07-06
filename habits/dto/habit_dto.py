import re
from habits.utils.date_utils import is_valid_cron

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ValidationError(Exception):
    pass


class CreateHabitDTO:
    def __init__(self, data: dict):
        self.title = (data.get("title") or "").strip()
        self.reminder_email = (data.get("reminder_email") or "").strip().lower()
        self.cron_expression = (data.get("cron_expression") or "").strip()
        self._validate()

    def _validate(self):
        if not self.title or len(self.title) < 2:
            raise ValidationError("Habit title must be at least 2 characters.")
        if not EMAIL_RE.match(self.reminder_email):
            raise ValidationError("A valid reminder_email is required.")
        if not self.cron_expression:
            raise ValidationError("A cron_expression is required, e.g. '0 9 * * *'.")
        if not is_valid_cron(self.cron_expression):
            raise ValidationError(
                f"'{self.cron_expression}' is not a valid cron expression. "
                f"Format: 'minute hour day month weekday', e.g. '*/15 * * * *' for every 15 minutes."
            )


class UpdateHabitDTO:
    """All fields optional — only provided ones get validated/updated."""
    def __init__(self, data: dict):
        self.title = data.get("title")
        self.reminder_email = data.get("reminder_email")
        self.cron_expression = data.get("cron_expression")
        self.is_active = data.get("is_active")
        self._validate()

    def _validate(self):
        if self.title is not None:
            self.title = self.title.strip()
            if len(self.title) < 2:
                raise ValidationError("Habit title must be at least 2 characters.")
        if self.reminder_email is not None:
            self.reminder_email = self.reminder_email.strip().lower()
            if not EMAIL_RE.match(self.reminder_email):
                raise ValidationError("A valid reminder_email is required.")
        if self.cron_expression is not None:
            self.cron_expression = self.cron_expression.strip()
            if not is_valid_cron(self.cron_expression):
                raise ValidationError(f"'{self.cron_expression}' is not a valid cron expression.")

    def to_update_dict(self) -> dict:
        fields = {}
        if self.title is not None:
            fields["title"] = self.title
        if self.reminder_email is not None:
            fields["reminder_email"] = self.reminder_email
        if self.cron_expression is not None:
            fields["cron_expression"] = self.cron_expression
        if self.is_active is not None:
            fields["is_active"] = bool(self.is_active)
        return fields