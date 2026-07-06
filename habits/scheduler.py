from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


def start():
    from habits.services.reminder_service import ReminderService

    scheduler = BackgroundScheduler(timezone="UTC")

    def job():
        ReminderService().run_reminders()

    # Checks every 60 seconds; each habit's own cron_expression decides if it actually fires.
    scheduler.add_job(job, IntervalTrigger(seconds=60), id="habit_reminder_checker", replace_existing=True)
    scheduler.start()