import datetime
from django.contrib.postgres.fields import JSONField, ArrayField, HStoreField
from django.db import models
from django.utils import timezone

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Persons(models.Model):
    name = models.CharField(max_length=32)
    gender = models.CharField(max_length=16, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    native_place = models.CharField(max_length=100, null=True, blank=True)
    id_card = models.CharField(max_length=18, unique=True, null=True)
    duty = models.CharField(max_length=100, null=True, blank=True)
    project_unit = JSONField(blank=True, null=True)
    team = models.CharField(max_length=100, null=True, blank=True)
    work = JSONField(blank=True, null=True)
    identity = models.IntegerField(default=0)
    images = JSONField(null=True, blank=True)
    certificate = JSONField(null=True, blank=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.name


class EnterOrLeaves(models.Model):
    person = models.OneToOneField(Persons, on_delete=models.CASCADE)
    enter_time = models.DateTimeField(null=True, blank=True)
    leave_time = models.DateTimeField(null=True, blank=True)
    enter_status = models.IntegerField(default=0)
    # create_on = models.DateTimeField(null=True, blank=True)
    # history = ArrayField(models.CharField(max_length=200), blank=True, null=True, default=[])
    history = JSONField(null=True, blank=True, default=[])

    @receiver(post_save, sender=Persons)
    def create_person_enterorleave(sender, instance=None, created=False, **kwargs):
        if created:
            EnterOrLeaves.objects.get_or_create(person=instance)











