import requests
from config import settings
from django.core.mail import send_mail


def send_tg_message(chat_id, habit):
    """
    Функция отправки сообщений через Telegram
    """
    url = f'{settings.TELEGRAM_API}{settings.TELEGRAM_BOT}/sendMessage'
    params = {
        'text': f'Пора выполнить привычку: {habit.action}',
        'chat_id': chat_id,
    }
    response = requests.get(url, params=params, timeout=10)
    if response.status_code != 200:
        print("TG ERROR:", response.text)


def send_email_message(email, habit):
    """
    Функция отправки сообщений через почту
    """
    subject = "Напоминание о привычке"
    message = f"Пора выполнить привычку: {habit.action}"

    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])