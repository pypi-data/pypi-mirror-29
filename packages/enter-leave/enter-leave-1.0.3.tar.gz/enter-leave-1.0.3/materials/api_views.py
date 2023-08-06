# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import datetime, calendar, requests
from django.db.models import Q, Count, Avg, Max, Min, Sum, QuerySet
from django.shortcuts import get_object_or_404
from pytz import utc
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import OrderingFilter
from . import models
from . import serializers
from comm.pagination import StandardPagination
from comm.filter import CustomSearchFilter, CustomSearchFilter1
from comm import permissions



class MaterialsListView(generics.ListCreateAPIView):
    queryset = models.Materials.objects.all()
    serializer_class = serializers.MaterialsSerializer

    # permission_classes = (IsAuthenticated,)
    # permission_classes = (permissions.IsAuthenticated,)
    # perms_map = {
    #     'GET': ['accounts.appmeta.MANAGE.NEWS.READ'],
    #     'POST': ['accounts.appmeta.MANAGE.NEWS.WRITE'],
    # }
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.MaterialsSerializerWhole
        else:
            return serializers.MaterialsSerializer


class MaterialsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Materials.objects.all()
    serializer_class = serializers.MaterialsSerializerWhole
    # permission_classes = (permissions.IsAuthenticated,)
    # perms_map = {
    #     'GET': ['accounts.appmeta.MANAGE.NEWS.READ'],
    #     'PUT': ['accounts.appmeta.MANAGE.NEWS.CREATE'],
    #     'DELETE': ['accounts.appmeta.MANAGE.NEWS.DELETE'],
    # }


class MaterialsSpecificationListView(generics.ListCreateAPIView):
    queryset = models.MaterialsSpecification.objects.all()
    serializer_class = serializers.MaterialsSpecificationSerializer

    # permission_classes = (IsAuthenticated,)
    # permission_classes = (permissions.IsAuthenticated,)
    # perms_map = {
    #     'GET': ['accounts.appmeta.MANAGE.NEWS.READ'],
    #     'POST': ['accounts.appmeta.MANAGE.NEWS.WRITE'],
    # }

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.MaterialsSpecificationSerializer
        else:
            return serializers.MaterialsSpecificationSerializerEdit

    def get_queryset(self):
        queryset = super(MaterialsSpecificationListView, self).get_queryset()
        material_code = self.request.GET.get('material_code')
        if material_code:
            queryset = queryset.filter(material__code=material_code)
            return queryset
        return queryset


class MaterialsSpecificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.MaterialsSpecification.objects.all()
    serializer_class = serializers.MaterialsSpecificationSerializer

    # permission_classes = (IsAuthenticated,)
    # permission_classes = (permissions.IsAuthenticated,)
    # perms_map = {
    #     'GET': ['accounts.appmeta.MANAGE.NEWS.READ'],
    #     'PUT': ['accounts.appmeta.MANAGE.NEWS.CREATE'],
    #     'DELETE': ['accounts.appmeta.MANAGE.NEWS.DELETE'],
    # }


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.MaterialsSpecificationSerializer
        else:
            return serializers.MaterialsSpecificationSerializerEdit


class MaterialEntryListView(generics.ListCreateAPIView):
    queryset = models.MaterialEntry.objects.all()
    serializer_class = serializers.MaterialEntrySerializer
    pagination_class = StandardPagination
    # permission_classes = (IsAuthenticated,)
    # permission_classes = (permissions.IsAuthenticated,)
    # perms_map = {
    #     'GET': ['accounts.appmeta.MANAGE.NEWS.READ'],
    #     'POST': ['accounts.appmeta.MANAGE.NEWS.WRITE'],
    # }
    filter_backends = (OrderingFilter, CustomSearchFilter1)
    ordering_fileds = ('create_on')
    search_params = [
        {'project_pk': 'project__pk__in'},
        {'project_code': 'project__code__in'},
        {'project_unit_pk': 'project_unit__pk__in'},
        {'project_unit_code': 'project_unit__code__in'},
        {'producer': 'producer__name__in'},
        {'created_year': 'create_on__year__in'},
        {'created_month': 'create_on__month__in'},
        {'created_date': 'create_on__date__in'},
        {'delivery_order': 'delivery_order__in'},
        {'lot_number': 'lot_number__in'},
        {'material': 'material__in'},
        {'spec': 'material_spec__name__in'}

    ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.MaterialEntrySerializer
        else:
            return serializers.MaterialEntrySerializerEdit

    def get_queryset(self):
        queryset = super(MaterialEntryListView, self).get_queryset()
        search_key = self.request.GET.get('keyword')

        if search_key:
            queryset = queryset.filter(Q(material__contains=search_key) \
                                       | Q(material_spec__code__contains=search_key) \
                                       | Q(material_spec__name__contains=search_key))
        return queryset

    def perform_create(self, serializer):
        material_spec = serializer.validated_data['material_spec']
        serializer.validated_data['material'] = material_spec.material.name
        serializer.save()


class MaterialEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.MaterialEntry.objects.all()
    serializer_class = serializers.MaterialEntrySerializer

    # permission_classes = (IsAdminUser,)
    # permission_classes = (permissions.IsAuthenticated,)
    # perms_map = {
    #     'GET': ['accounts.appmeta.MANAGE.NEWS.READ'],
    #     'PUT': ['accounts.appmeta.MANAGE.NEWS.CREATE'],
    #     'DELETE': ['accounts.appmeta.MANAGE.NEWS.DELETE'],
    # }

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.MaterialEntrySerializer
        else:
            return serializers.MaterialEntrySerializerEdit

    def perform_update(self, serializer):
        material_spec = serializer.validated_data['material_spec']
        if material_spec:
            serializer.validated_data['material'] = material_spec.material.name

        serializer.save()


# class MaterialStatisticsView(APIView):
#     def get(self, request):
#
#            cursor = connection.cursor()
#
#            cursor.execute('select material_spec_id, sum(material_count) from materials_materialsentry group by material_spec_id')
#
#            list = cursor.fetchall()
#            data = []
#            for elem in list:
#                k, v = elem
#                spec = models.MaterialSpecification.objects.get(id=k)
#                data.append({'material':spec.material.name, 'spec':spec.name, 'total':v})
#
#            return Response(data)

class MaterialStatisticsView(APIView):
    # serializer_class = serializers.MaterialsStatisticSerializer
    def get(self, request):
        queryset = models.MaterialEntry.objects.all()
        query_params = self.request.query_params
        try:
            if query_params.get('project'):
                queryset = queryset.filter(project__pk=query_params['project'])
            if query_params.get('project_unit'):
                queryset = queryset.filter(project_unit__pk=query_params['project_unit'])
            if query_params.get('materialstatistic'):
                queryset = queryset.values('project', 'project_unit', 'material_spec', 'material', 'material_count')\
                    .annotate(value=Sum('material_count'), count=Count('material'))\
                    .values('project', 'project_unit', 'material_spec__name', 'material_spec__material__name', 'value', 'count')
            if query_params.get('monthstatistics'):
                time_range = query_params.get('time_range')
                if time_range:
                    slice_list = time_range.replace(' ', '').split(',')
                    if len(slice_list) == 2:
                        from_date = datetime.datetime.strptime(slice_list[0], "%Y-%m-%d").replace(tzinfo=utc)
                        to_date = datetime.datetime.strptime(slice_list[1], "%Y-%m-%d").replace(tzinfo=utc)
                        queryset = queryset.filter(create_on__range=(from_date, to_date))

                queryset = queryset.extra(select={'month':"to_char(create_on,'YYYY-MM')"}).values('project', 'project_unit','material', 'material_count','month') \
                    .annotate(value=Sum('material_count'), count=Count('material')) \
                    .values('project','project_unit', 'month', 'material', 'value', 'count')
                # for e in queryset:
                #  print type(e.get('project').get('name'))

            return Response(queryset)
        except Exception, e:
            print str(e)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)






