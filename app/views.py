from itertools import cycle

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import View

import requests
from requests.exceptions import ConnectionError

from .google_analytics import get_access_token
from .uptime_robot import UptimeRobot
from .models import Service
from .models import GoogleAnalyticsSite


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


class SpotligthView(LoginRequiredMixin, View):
    SPOTLIGTH_CYCLE = cycle('AB')

    def get(self, request, *args, **kwargs):
        case = next(self.SPOTLIGTH_CYCLE)
        if case == 'A':
            obj = Service.objects.all().order_by('?').first()
            if not obj:
                raise Http404('Create a Service first')

            return render(request, 'service_detail.html', {
                'obj': obj,
            })

        elif case == 'B':
            obj = GoogleAnalyticsSite.objects.all().order_by('?').first()
            if not obj:
                raise Http404('Create a GoogleAnalyticsSite first')

            return render(request, 'googleanalyticssite_detail.html', {
                'ACCESS_TOKEN': get_access_token(),
                'obj': obj,
            })


class TickerView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response_list = []

        # Zendesk
        zendesk_data = cache.get('zendesk_data')
        if not zendesk_data:
            try:
                req = requests.get(
                    settings.ZENDESK_URL,
                    auth=(settings.ZENDESK_EMAIL, settings.ZENDESK_API),
                )
                if req.ok:
                    zendesk_data = {
                        'title': 'Tickets',
                        'label': 'Zendesk',
                        'value': req.json()['view_count']['value'],
                    }
                    cache.set('zendesk_data', zendesk_data, 120)
            except ConnectionError:
                zendesk_data = None

        if zendesk_data:
            response_list.append(zendesk_data)

        # Sentry
        sentry_data = cache.get('sentry_data')
        if not sentry_data:
            try:
                req = requests.get(
                    settings.SENTRY_URL,
                    auth=(settings.SENTRY_KEY, ''),
                )
                if req.ok:
                    sentry_data = {
                        'title': 'Events',
                        'label': 'Sentry',
                        'value': sum([x[1] for x in req.json()]),
                    }
                    cache.set('sentry_data', sentry_data, 60)
            except ConnectionError:
                sentry_data = None

        if sentry_data:
            response_list.append(sentry_data)

        # Uptime Robot
        monitor_list = cache.get('monitor_list')
        if not monitor_list:
            uptime_robot = UptimeRobot()
            success, response = uptime_robot.get_monitors()
            if success:
                monitor_list = []
                for monitor in response.get('monitors').get('monitor'):
                    monitor_list.append({
                        'title': monitor.get('friendlyname'),
                        'label': 'Uptime',
                        'value': '{0}%'.format(
                            monitor.get('customuptimeratio')
                        ),
                    })
                cache.set('monitor_list', monitor_list, 90)

        if monitor_list:
            response_list.extend(monitor_list)

        return render(request, 'ticker_detail.html', {
            'response_list': response_list,
        })
