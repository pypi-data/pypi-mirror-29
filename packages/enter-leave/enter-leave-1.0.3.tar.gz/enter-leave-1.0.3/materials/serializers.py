#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, json
from django.conf import settings
from django.contrib.auth.models import User, Group, Permission
from django.db.models.fields import related_descriptors

from rest_framework import serializers

from . import models

headers = {'content_type': 'application/json'}


class MaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Materials
        fields = ('id', 'name', 'code', 'unit')


class MaterialsSerializerWhole(serializers.ModelSerializer):
    class Meta:
        model = models.Materials
        fields = ('id', 'name', 'code', 'material_spec')

    def to_representation(self, instance):
        data = super(MaterialsSerializerWhole, self).to_representation(instance)
        data['material_spec'] = []
        for elem in models.MaterialsSpecification.objects.filter(material=instance):
            data['material_spec'].append({'id': elem.id, 'code': elem.name, 'name': elem.code})
        return data



class MaterialsSpecificationSerializer(serializers.ModelSerializer):
    material = MaterialsSerializer()

    class Meta:
        model = models.MaterialsSpecification
        fields = '__all__'


class MaterialsSpecificationSerializerEdit(serializers.ModelSerializer):
    class Meta:
        model = models.MaterialsSpecification
        fields = '__all__'


class MaterialEntrySerializer(serializers.ModelSerializer):
    material_spec = MaterialsSpecificationSerializer()

    class Meta:
        model = models.MaterialEntry
        fields = '__all__'

        # def create(self, validated_data):


class MaterialEntrySerializerEdit(serializers.ModelSerializer):
    class Meta:
        model = models.MaterialEntry
        fields = '__all__'


