import os

from django.db import models
from django.urls import reverse_lazy


class Subject(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


def get_account_path(instance, filename):
    path = str(instance.id)
    return os.path.join(path, filename)


class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to=get_account_path, null=True, blank=True)
    email_address = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=14)
    room_number = models.CharField('Room Number', max_length=100)
    subjects_taught = models.ManyToManyField(Subject)

    def __str__(self):
        return "%s %s" % (self.first_name,self.last_name)

    def get_detail_url(self):
        return reverse_lazy('directory:teacher-detail', kwargs={'pk':self.id})