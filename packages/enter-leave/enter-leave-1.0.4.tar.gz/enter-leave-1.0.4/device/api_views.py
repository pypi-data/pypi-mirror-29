#-*- coding:utf-8 -*-
from __future__ import unicode_literals
import datetime, calendar, requests
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.http import Http404
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
from comm.pagination import StandardPagination

class DeviceMobilityListView(generics.ListCreateAPIView):
    queryset = models.DeviceMobilitys.objects.all()
    serializer_class = serializers.DeviceMobilitysSerializer
    pagination_class = StandardPagination
    filter_backends = (OrderingFilter, CustomSearchFilter1)
    ordering_fields = ('created_on', 'end_on')
    search_params = [
        {'project_pk': 'project__pk__in'},
        {'project_code': 'project__code__in'},
        {'project_unit_pk': 'project_unit__pk__in'},
        {'project_unit_code': 'project_unit__code__in'},
        {'created_year': 'created_on__year__in'},
        {'created_month': 'created_on__month__in'},
        {'created_date': 'created_on__date__in'},
        {'source': 'source__in'},
        {'manufacturer_name': 'manufacturer__name__in'}
    ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DeviceMobilitysDetailSerializer
        else:
            return serializers.DeviceMobilitysSerializer

    def get_queryset(self):
        queryset = super(DeviceMobilityListView, self).get_queryset()
        search_key = self.request.GET.get('keyword')
        is_ground = self.request.GET.get('ground')
        if is_ground:
            queryset = queryset.filter(is_ground__exact=is_ground)
        if search_key:
            queryset = queryset.filter(Q(device_name__name__contains=search_key) \
                |Q(device_spec__contains=search_key) \
                |Q(device_type__contains=search_key))
        return queryset

class DeviceMobilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.DeviceMobilitys.objects.all()
    serializer_class = serializers.DeviceMobilitysSerializer
    # permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.DeviceMobilitysDetailSerializer
        else:
            return serializers.DeviceMobilitysSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        if serializer.validated_data.get('is_ground') is not True:
            if serializer.validated_data.get('end_on') is None:
                instance.end_on = datetime.datetime.now()
                instance.save()

class DeviceListView(generics.ListCreateAPIView):
    queryset = models.Devices.objects.all()
    serializer_class = serializers.DevicesSerializer

class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Devices.objects.all()
    serializer_class = serializers.DevicesSerializer


class DeviceCalculation(APIView):

    def get(self, request):
        keyword = self.request.query_params.get('keyword')
        is_ground = self.request.query_params.get('is_ground')
        enter_time_slice = self.request.query_params.get('enter_time_slice')
        leave_time_slice = self.request.query_params.get('leave_time_slice')

        queryset = models.DeviceMobilitys.objects.all()

        if leave_time_slice:
            slice_list = leave_time_slice.replace(' ', '').split(',')
            if len(slice_list) == 2:
                try:
                    enter_time_from = datetime.datetime.strptime(slice_list[0], "%Y-%m-%d").replace(tzinfo=utc)
                    enter_time_to = datetime.datetime.strptime(slice_list[1], "%Y-%m-%d").replace(tzinfo=utc)
                except Exception as e:
                    raise Http404
                queryset = queryset.filter(end_on__range=(enter_time_from, enter_time_to),
                                               is_ground=False)
            if not keyword:
                return Response({'count': queryset.count(), 'info': queryset.values()})
            else:
                return Response(queryset.values(keyword).annotate(count=Count(keyword)))

        if enter_time_slice:
            slice_list = enter_time_slice.replace(' ', '').split(',')
            if len(slice_list) == 2:
                try:
                    enter_time_from = datetime.datetime.strptime(slice_list[0], "%Y-%m-%d").replace(tzinfo=utc)
                    enter_time_to = datetime.datetime.strptime(slice_list[1], "%Y-%m-%d").replace(tzinfo=utc)
                except Exception as e:
                    raise Http404

                if is_ground == 'true':
                    queryset = queryset.filter(created_on__range=(enter_time_from, enter_time_to),
                                               is_ground=True)
                if is_ground == 'false':
                    queryset = queryset.filter(created_on__range=(enter_time_from, enter_time_to),
                                               is_ground=False)
                else:
                    queryset = queryset.filter(created_on__range=(enter_time_from, enter_time_to))
        else:
            if is_ground == 'true':
                queryset = queryset.filter(is_ground=True)
            if is_ground == 'false':
                queryset = queryset.filter(is_ground=False)

        if not keyword:
            return Response({'count': queryset.count(), 'info': queryset.values()})
        else:
            return Response(queryset.values(keyword).annotate(count=Count(keyword)))


