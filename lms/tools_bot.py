import datetime, pytz
from django.utils import timezone

def format_text(date, tz=pytz.timezone("Europe/Moscow")):
    text = "Your next class will be on "
    fmt = "%A, %H:%M (%d %B)"
    timezone.activate(tz)
    text += date.strftime(fmt)
    return text