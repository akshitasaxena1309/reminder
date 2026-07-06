from bson import ObjectId
from accounts.db.connection import get_db
from habits.models.habit_model import Habit


class HabitRepository:
    def __init__(self):
        self.collection = get_db()["habits"]
        self.collection.create_index("user_id")

    def create(self, habit: Habit) -> Habit:
        result = self.collection.insert_one(habit.to_document())
        habit.id = str(result.inserted_id)
        return habit

    def find_by_id(self, habit_id: str):
        try:
            doc = self.collection.find_one({"_id": ObjectId(habit_id)})
        except Exception:
            return None
        return Habit.from_document(doc) if doc else None

    def find_all_by_user(self, user_id: str) -> list:
        docs = self.collection.find({"user_id": user_id}).sort("created_at", -1)
        return [Habit.from_document(d) for d in docs]

    def find_all_active(self) -> list:
        """Used by the reminder job — every active habit, across all users."""
        docs = self.collection.find({"is_active": True})
        return [Habit.from_document(d) for d in docs]

    def update_fields(self, habit_id: str, fields: dict) -> bool:
        if not fields:
            return False
        result = self.collection.update_one({"_id": ObjectId(habit_id)}, {"$set": fields})
        return result.matched_count > 0

    def update_last_sent(self, habit_id: str, sent_at):
        self.collection.update_one({"_id": ObjectId(habit_id)}, {"$set": {"last_sent_at": sent_at}})

    def delete(self, habit_id: str, user_id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(habit_id), "user_id": user_id})
        return result.deleted_count > 0