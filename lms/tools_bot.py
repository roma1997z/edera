import datetime, pytz
from django.utils import timezone
from django.conf import settings

def format_text(date, duration, student_name, subject_name="English", teacher_name="Someone",
                tz=pytz.timezone(settings.TIME_ZONE)):

    text = "Dear {},\n\n".format(student_name)
    text += "Just a kind reminder of your {} class on ".format(subject_name)
    fmt = "%A (%d %B)"
    text += date.astimezone(tz).strftime(fmt)

    time_fmt = "%H:%M"
    end_time = date + datetime.timedelta(minutes=duration)
    text += "\n\n"
    text = text + date.astimezone(tz).strftime(time_fmt)+"-"+end_time.astimezone(tz).strftime(time_fmt) + "* " + subject_name + " ({})".format(teacher_name)
    text += "\n\n"
    text += "*Moscow Time Zone"
    text += "\n\n"
    text += "Have a great day!"
    return text