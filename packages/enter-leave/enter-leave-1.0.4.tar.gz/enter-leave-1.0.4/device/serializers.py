#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, json
from django.conf import settings
from django.contrib.auth.models import User, Group, Permission

from rest_framework import serializers

from . import models

class DevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Devices
        fields = ('id', 'name', 'code')

class DeviceMobilitysSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeviceMobilitys
        fields = ("id", "project", "project_unit", "construction_org", "construction_per",
                  "supervising_org", "supervising_per", "device_name", "number", "device_type",
                  "device_spec", "original_value", "source", "manufacturer", "licence", "end_on",
                  "certificate", "attachments", "remark_one", "is_ground", "images", "created_on")

class DeviceMobilitysDetailSerializer(DeviceMobilitysSerializer):
    device_name = DevicesSerializer(many=False)
