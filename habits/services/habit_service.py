from habits.repositories.habit_repository import HabitRepository
from habits.models.habit_model import Habit


class HabitError(Exception):
    pass


class HabitService:
    def __init__(self):
        self.habit_repo = HabitRepository()

    def create_habit(self, user_id: str, dto) -> dict:
        habit = Habit(
            user_id=user_id,
            title=dto.title,
            reminder_email=dto.reminder_email,
            cron_expression=dto.cron_expression,
        )
        habit = self.habit_repo.create(habit)
        return habit.public_dict()

    def list_habits(self, user_id: str) -> list:
        return [h.public_dict() for h in self.habit_repo.find_all_by_user(user_id)]

    def get_habit(self, habit_id: str, user_id: str) -> dict:
        habit = self._get_owned(habit_id, user_id)
        return habit.public_dict()

    def update_habit(self, habit_id: str, user_id: str, dto) -> dict:
        habit = self._get_owned(habit_id, user_id)
        fields = dto.to_update_dict()
        if fields:
            self.habit_repo.update_fields(habit_id, fields)
        return self.get_habit(habit_id, user_id)

    def delete_habit(self, habit_id: str, user_id: str):
        if not self.habit_repo.delete(habit_id, user_id):
            raise HabitError("Habit not found.")

    def _get_owned(self, habit_id: str, user_id: str) -> Habit:
        habit = self.habit_repo.find_by_id(habit_id)
        if not habit or habit.user_id != user_id:
            raise HabitError("Habit not found.")
        return habit