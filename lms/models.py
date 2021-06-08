from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True)

    role = models.CharField(max_length=16, default="student")
    photo = models.ImageField(upload_to="user", blank=True, null=True)

    phone = models.CharField(max_length=32, blank=True, null=True)
    vk = models.CharField(max_length=32, blank=True, null=True)
    tg = models.CharField(max_length=32, blank=True, null=True)
    fb = models.CharField(max_length=32, blank=True, null=True)

    active = models.IntegerField(default=1, blank=True,null=True)
    moderator = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.user_id)


class InterestKey(models.Model):
    note_id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=16)
    name = models.CharField(max_length=64)

    important = models.FloatField(default=1.0, blank=True, null=True)
    active = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.key


class Interest(models.Model):
    note_id = models.AutoField(primary_key=True)

    key = models.ForeignKey(InterestKey, on_delete=models.CASCADE) #grade, exam
    symbol = models.CharField(max_length=16, null=True, blank=True)
    name = models.CharField(max_length=64) #options
    desc = models.TextField(blank=True, null=True) #help if needed

    important = models.FloatField(default=1.0, blank=True, null=True)
    active = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)


class InterestUser(models.Model):
    note_id = models.AutoField(primary_key=True)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)

    date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    def __str__(self):
        return "{}-{}".format(self.user_id.username, self.interest.name)


class MatchUser(models.Model):
    note_id = models.AutoField(primary_key=True)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher')

    date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    like = models.BooleanField(default=True, blank=True)
    active = models.BooleanField(default=True, blank=True)


# Учитель, ученик, чат
class UserTeacher(models.Model):
    note_id = models.AutoField(primary_key=True)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conn_user_id')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conn_teacher')
    chat_id = models.IntegerField(null=True, blank=True)

    date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    active = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.user_id.first_name + " (" + self.teacher.first_name+ ")"


# Запланированные уроки с учеником
class Lesson(models.Model):
    note_id = models.AutoField(primary_key=True)

    conn = models.ForeignKey(UserTeacher, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField(default=120) #in minutes
    name = models.CharField(max_length=64, default="English Language")
    notification = models.BooleanField(default=False)
    repeat = models.BooleanField(default=False)

    active = models.IntegerField(default=1) #0 - stopped, 1 - accepted, 2 - waiting for response


class TeacherTime(models.Model):
    note_id = models.AutoField(primary_key=True)

    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()


class LessonBook(models.Model):
    note_id = models.AutoField(primary_key=True)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.IntegerField(default=0)

    day_0 = models.BooleanField(default=False, blank=True) #0-7
    day_1 = models.BooleanField(default=False, blank=True)
    day_2 = models.BooleanField(default=False, blank=True)
    day_3 = models.BooleanField(default=False, blank=True)
    day_4 = models.BooleanField(default=False, blank=True)
    day_5 = models.BooleanField(default=False, blank=True)
    day_6 = models.BooleanField(default=False, blank=True)
    day_7 = models.BooleanField(default=False, blank=True)

    date = models.DateTimeField(default=timezone.now) # when ordered
    active = models.IntegerField(default=1)



class TeacherKey(models.Model):
    note_id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=16)
    name = models.CharField(max_length=64)

    important = models.FloatField(default=1.0, blank=True, null=True)
    active = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.key


class TeacherDesc(models.Model):
    note_id = models.AutoField(primary_key=True)

    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="desc_teacher")
    key = models.ForeignKey(TeacherKey, on_delete=models.CASCADE)
    text = models.TextField()

    active = models.BooleanField(default=True, blank=True)

