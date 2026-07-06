from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class User:
    name: str
    email: str
    password: str  # always the HASHED password, never plaintext
    id: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_document(self) -> dict:
        """Convert entity -> dict for inserting into MongoDB (no _id field)."""
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_document(doc: dict) -> "User":
        """Convert a MongoDB document -> User entity."""
        return User(
            id=str(doc["_id"]),
            name=doc["name"],
            email=doc["email"],
            password=doc["password"],
            created_at=doc.get("created_at"),
        )

    def public_dict(self) -> dict:
        """Safe representation for API responses — never expose password."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }