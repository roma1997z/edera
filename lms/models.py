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


class TeacherTime(models.Model):
    note_id = models.AutoField(primary_key=True)

    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()


class Lesson(models.Model):
    note_id = models.AutoField(primary_key=True)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_user_id')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_teacher')

    day = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()


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

