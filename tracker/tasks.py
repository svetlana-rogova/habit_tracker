from celery import shared_task
from django.utils import timezone

from tracker.models import Habit
from tracker.services import send_email_message
from tracker.services import send_tg_message


@shared_task
def send_message():
    """
    Задача на отправку сообщения через Telegram и почту
    """
    now = timezone.localtime()
    print("TASK STARTED")
    habits = Habit.objects.filter(time__hour=now.hour, time__minute=now.minute)
    print("HABITS FOUND:", list(habits))

    for habit in habits:
        try:
            send_tg_message(habit.owner.chat_id, habit)
        except Exception as e:
            print("TG FAILED:", e)
        user_email = habit.owner.email
        if user_email:
            print("TRY SEND EMAIL")
            try:
                send_email_message(user_email, habit)
                print("EMAIL SENT SUCCESS")
            except Exception as e:
                print("EMAIL ERROR:", e)
        else:
            print("NO EMAIL FOR USER")
