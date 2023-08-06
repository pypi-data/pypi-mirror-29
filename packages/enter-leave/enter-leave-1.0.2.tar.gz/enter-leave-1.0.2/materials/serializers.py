#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, json
from django.conf import settings
from django.contrib.auth.models import User, Group, Permission
from django.db.models.fields import related_descriptors

from rest_framework import serializers

from . import models

headers = {'content_type': 'application/json'}


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Material
        fields = ('id', 'name', 'code', 'unit')


class MaterialSerializerWhole(serializers.ModelSerializer):
    class Meta:
        model = models.Material
        fields = ('id', 'name', 'code', 'material_spec')

    def to_representation(self, instance):
        data = super(MaterialSerializerWhole, self).to_representation(instance)
        data['material_spec'] = []
        for elem in models.MaterialSpecification.objects.filter(material=instance):
            data['material_spec'].append({'id': elem.id, 'code': elem.name, 'name': elem.code})
        return data



class MaterialSpecificationSerializer(serializers.ModelSerializer):
    material = MaterialSerializer()

    class Meta:
        model = models.MaterialSpecification
        fields = '__all__'


class MaterialSpecificationSerializerEdit(serializers.ModelSerializer):
    class Meta:
        model = models.MaterialSpecification
        fields = '__all__'


class MaterialsEntrySerializer(serializers.ModelSerializer):
    material_spec = MaterialSpecificationSerializer()

    class Meta:
        model = models.MaterialsEntry
        fields = '__all__'

        # def create(self, validated_data):


class MaterialsEntrySerializerEdit(serializers.ModelSerializer):
    class Meta:
        model = models.MaterialsEntry
        fields = '__all__'


