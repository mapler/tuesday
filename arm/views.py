# -*- coding: utf-8 -*-
import json
from django.views.generic import TemplateView, View
from django.http import HttpResponse
from arm.constants import BASE_DURATION
from arm.models import ArmManager


class ArmIndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, message=u'', **kwargs):
        part_ids = ArmManager.parts.keys()

        return {
            'arm_manager': ArmManager,
            'message': message,
            'part_ids': part_ids,
            'BASE_DURATION': BASE_DURATION,
        }


class ArmApiView(View):

    @staticmethod
    def _response_json(context):
        """
        return a json type response
        """
        return HttpResponse(json.dumps(context), content_type="application/json")

    def get_context_data(self, part_ids, message=u''):
        """
        collect parts status and make into a dict
        """
        response_data = dict()
        response_data['is_on'] = ArmManager.is_on()
        parts_status = []
        for part_id in part_ids:
            part = ArmManager.get_part(part_id)
            parts_status.append({'part_id': part_id, 'position': part.status.position})

        response_data['parts_status'] = parts_status
        response_data['message'] = message
        return response_data

    def get(self, request, part_id=None):
        """
        part status api
        return a json response of parts status and device status
        """
        if part_id:
            part_id = int(part_id)
            if part_id in ArmManager.parts.keys():
                part_ids = [part_id]
            else:
                part_ids = []
        else:
            part_ids = ArmManager.parts.keys()

        context = self.get_context_data(part_ids)
        return self._response_json(context)

    def post(self, request, part_id=None):
        """
        part action api
        move the part and change status,
        return a json response of parts status and device status
        """
        duration = request.POST.get('duration', 0)
        part_ids = ArmManager.parts.keys()
        message = ''

        if part_id and duration:
            part_id = int(part_id)
            duration = int(duration)

            action = request.POST.get('action')
            try:
                is_acted = getattr(ArmManager, action)(part_id, duration)
            except AttributeError:
                is_acted = False

            if is_acted:
                message = u'ACTED.'

        context = self.get_context_data(part_ids, message)
        return self._response_json(context)
