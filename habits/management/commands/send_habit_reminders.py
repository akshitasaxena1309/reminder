from django.core.management.base import BaseCommand
from habits.services.reminder_service import ReminderService


class Command(BaseCommand):
    help = "Check all active habits' cron schedules and send due reminder emails."

    def handle(self, *args, **options):
        ReminderService().run_reminders()
        self.stdout.write("Reminder check completed.");