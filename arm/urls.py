# -*— coding: utf-8 -*-
from django.conf.urls import url, patterns
from views import ArmIndexView, ArmApiView

urlpatterns = patterns('arm',
                       url(r'^$', ArmIndexView.as_view(), name='arm_index'),
                       url(r'^arm/status/$', ArmApiView.as_view(), name='arm_part_status'),
                       url(r'^arm/status/(?P<part_id>\d+)/$', ArmApiView.as_view(), name='arm_part_status'),
                       )
