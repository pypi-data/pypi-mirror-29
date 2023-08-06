# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField, HStoreField, ArrayField

# Create your models here.


class Materials(models.Model):
    code = models.CharField(max_length=128, blank=True, null=True, unique=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    unit = models.CharField(max_length=128, blank=True, null=True)
    material_spec = JSONField(null=True, blank=True)
    def __unicode__(self):
        return '{0}-{1}'.format(self.code, self.name)

class MaterialsSpecification(models.Model):
    code = models.CharField(max_length=128, blank=True, null=True,  unique=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    material = models.ForeignKey(Materials, blank=True, null=True)

    def __unicode__(self):
        return self.name

class MaterialEntry(models.Model):
    project = JSONField(blank=True, null=True)
    project_unit = JSONField(blank=True, null=True)
    constructionorg = JSONField(blank=True, null=True)
    responsor = JSONField(blank=True, null=True)
    responsor_org = JSONField(blank=True, null=True)
    delivery_order = models.CharField(max_length=128, null=True, blank=True)
    lot_number = models.CharField(max_length=128, null=True, blank=True)
    remark = models.TextField(max_length=255, blank=True, null=True)
    material = models.CharField(max_length=123, blank=True, null=True)
    material_spec = models.ForeignKey(MaterialsSpecification, null=True, blank=True)
    material_count = models.IntegerField(blank=True, null=True, default=1)
    material_value = models.FloatField(blank=True, null=True, default=0.0)
    material_image = JSONField(null=True, blank=True)
    producer = JSONField(null=True, blank=True)
    supplier = models.CharField(max_length=128, null=True, blank=True)
    location = JSONField(null=True, blank=True)
    create_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '{0}--{1}--{2}'.format(self.material, self.material_spec.name, self.material_count)

    # class Meta:
    #     ordering = ['create_on']










