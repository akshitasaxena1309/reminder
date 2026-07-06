from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Habit:
    user_id: str
    title: str
    reminder_email: str
    cron_expression: str          # raw cron string, e.g. "*/30 * * * *"
    id: Optional[str] = None
    is_active: bool = True
    last_sent_at: Optional[datetime] = None   # UTC, used to avoid duplicate sends in the same minute
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_document(self) -> dict:
        return {
            "user_id": self.user_id,
            "title": self.title,
            "reminder_email": self.reminder_email,
            "cron_expression": self.cron_expression,
            "is_active": self.is_active,
            "last_sent_at": self.last_sent_at,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_document(doc: dict) -> "Habit":
        return Habit(
            id=str(doc["_id"]),
            user_id=doc["user_id"],
            title=doc["title"],
            reminder_email=doc["reminder_email"],
            cron_expression=doc["cron_expression"],
            is_active=doc.get("is_active", True),
            last_sent_at=doc.get("last_sent_at"),
            created_at=doc.get("created_at"),
        )

    def public_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "reminder_email": self.reminder_email,
            "cron_expression": self.cron_expression,
            "is_active": self.is_active,
            "last_sent_at": self.last_sent_at.isoformat() if self.last_sent_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }