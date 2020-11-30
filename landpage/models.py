from django.db import models
from django.utils import timezone
from django import forms
# Create your models here.
class TextTZ(models.Model):
    text_id = models.AutoField(primary_key=True)
    text_name = models.CharField(max_length=100)
    text = models.TextField(blank=True, null=True)
    active = models.IntegerField(default = 1)
    
    lang = models.CharField(max_length=100, default = 'rus')
    
class MyOption(models.Model):
    note_id = models.AutoField(primary_key = True)
    
    key= models.CharField(max_length = 100)
    text = models.TextField()
    
    date = models.DateTimeField(blank=True, default=timezone.now)
    active = models.IntegerField(default = 1)
    period = models.CharField(default = "all", max_length = 100)
    
class TeachersTZ(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    
    name = models.CharField(max_length=100)
    
    subject = models.CharField(max_length=300, blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    position = models.TextField(blank=True, null=True)
    interest = models.TextField(blank=True, null=True)
    
    description = models.TextField(blank=True, null=True)
    photo = models.CharField(max_length=100, blank=True, null=True)
    orderindex = models.IntegerField(default = 0)
    
    lang = models.CharField(max_length=100, default = 'rus')
    active = models.IntegerField(default = 1)
    #vk = models.CharField(max_length=100,  blank=True, null=True)
    
class University(models.Model):
    note_id = models.AutoField(primary_key=True)
    
    name = models.CharField(max_length=100)
    photo = models.CharField(max_length=100, blank=True, null=True)
    number = models.IntegerField(default = 1)
    
    orderindex = models.IntegerField(default = 0)
    
    active = models.IntegerField(default = 1)

class Contact(models.Model):
    note_id = models.AutoField(primary_key=True)
    
    name = models.CharField(max_length = 200)
    from_email = models.EmailField(blank = True, null = True)
    phone = models.CharField(max_length=12, blank = True, null = True)
    subject = models.CharField(max_length = 200, blank = True, null = True)
    message = models.TextField()
    
    date = models.DateTimeField(blank=True, default=timezone.now)

class ContactForm(forms.ModelForm):
    name = forms.CharField(required = False)
    subject = forms.CharField(required = False)
    message = forms.CharField(required = False)
    class Meta:
        model = Contact
        fields = ['name', 'from_email', 'subject', 'message']

class Quiz(models.Model):
    note_id = models.AutoField(primary_key=True)

    name = models.CharField(max_length = 200)
    data = models.FileField(upload_to="quiz")
    date = models.DateTimeField(blank=True, default=timezone.now)

class QuizResult(models.Model):
    note_id = models.AutoField(primary_key=True)

    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    email = models.CharField(max_length = 64)
    result = models.TextField()

    date = models.DateTimeField(blank=True, default=timezone.now)

class PersonReport(models.Model):
    note_id = models.AutoField(primary_key=True)

    photo = models.ImageField(upload_to="person")

    name = models.CharField(max_length=200)

    video_link = models.CharField(max_length=300, blank=True, null=True)
    desc = models.TextField()

    lang = models.CharField(max_length=100, default='rus')
    active = models.BooleanField(default=True, blank=True)