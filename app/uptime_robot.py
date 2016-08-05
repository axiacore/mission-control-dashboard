import json
from urllib import request

from django.conf import settings


class UptimeRobot(object):
    def __init__(self):
        self.api_key = settings.UPTIME_ROBOT_KEY
        self.base_url = settings.UPTIME_ROBOT_URL

    def get_monitors(self, response_times=0, logs=0, uptime_ratio=''):
        """
        Returns status and response payload for all known monitors.
        """
        url = self.base_url
        url += 'getMonitors?apiKey={0}'.format(self.api_key)
        url += '&noJsonCallback=1&format=json'
        # responseTimes - optional (defines if the response time data of each
        # monitor will be returned. Should be set to 1 for getting them. Default
        # is 0)
        if response_times:
            url += '&responseTimes=1'
        # logs - optional (defines if the logs of each monitor will be returned.
        # Should be set to 1 for getting the logs. Default is 0)
        if logs:
            url += '&logs=1'
        # customUptimeRatio - optional (defines the number of days to calculate
        # the uptime ratio(s) for. Ex: customUptimeRatio=7-30-45 to get the
        # uptime ratios for those periods)
        if uptime_ratio:
            url += '&customUptimeRatio={0}'.format(uptime_ratio)

        # Verifying in the response is jsonp in otherwise is error
        response = request.urlopen(url)
        content = response.read().decode('utf-8')
        j_content = json.loads(content)
        if j_content.get('stat'):
            stat = j_content.get('stat')
            if stat == "ok":
                return True, j_content
        return False, j_content
