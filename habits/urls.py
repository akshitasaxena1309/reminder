from django.urls import path
from habits.controllers import habit_controller as c

urlpatterns = [
    path("reminders/add/", c.add_reminder_page, name="add_reminder_page"),

    path("api/habits/", c.habits_collection, name="habits_collection"),
    path("api/habits/<str:habit_id>/", c.habit_detail, name="habit_detail"),

    path("api/cron/trigger-reminders/", c.trigger_reminders, name="trigger_reminders"),
]