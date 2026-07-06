import logging
from django.core.mail import send_mail
from django.conf import settings

from habits.repositories.habit_repository import HabitRepository
from habits.utils.date_utils import current_minute, is_due, already_sent_this_minute

logger = logging.getLogger(__name__)


class ReminderService:
    def __init__(self):
        self.habit_repo = HabitRepository()

    def run_reminders(self):
        now = current_minute()
        habits = self.habit_repo.find_all_active()

        for habit in habits:
            try:
                print(f"processing for {habit.title} (cron={habit.cron_expression}, now_utc={now})")

                if already_sent_this_minute(habit.last_sent_at, now):
                    print(f"already sent for {habit.title}")
                    continue

                if not is_due(habit.cron_expression, now):
                    print(f"not due for {habit.title}")
                    continue

                send_mail(
                    subject="Message From Akshita",
                    message=f"Hey, \n\n{habit.title}\n",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[habit.reminder_email],
                    fail_silently=False,
                )
                self.habit_repo.update_last_sent(habit.id, now)
                print(f"sent for {habit.title}")
            except Exception as e:
                print(f"Failed to send reminder for habit {habit.title}: {e}")