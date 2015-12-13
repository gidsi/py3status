# -*- coding: utf-8 -*-
"""
Display your next shift in the engelsystem, used on most chaos events

Configuration Parameters:
    - cache_timeout: Set timeout between calls in seconds
    - api_key: Your API Key, usualy part of the url
    - url: URL found on your engelsystem profile -> JSON export

@author timmszigat
@license WTFPL <http://www.wtfpl.net/txt/copying/>
"""

import codecs
import datetime
import json
from time import time
import urllib.request


class Py3status:
    """
    """
    # available configuration parameters
    cache_timeout = 60
    api_key = ''
    url = 'https://www.engelsystem.de/32c3/?p=shifts_json_export&key='

    def check(self, i3s_output_list, i3s_config):

        response = {
            'cached_until': time() + self.cache_timeout
            }

        try:
            # grab json file
            json_file = urllib.request.urlopen(self.url + self.api_key)
            reader = codecs.getreader("utf-8")
            shifts = json.load(reader(json_file))
            json_file.close()

            next_shift = None
            current_shift = None

            # gathering data
            for shift_raw in shifts:
                shift = {
                    'start': float(shift_raw['start']),
                    'end': float(shift_raw['end']),
                    'room_name': shift_raw['room_name']
                }
                if shift['start'] > time():
                    if not next_shift or next_shift and next_shift['start'] > shift['start']:
                        next_shift = shift

                elif shift['end'] < time():
                    current_shift = shift


            # display what was gathered
            if current_shift:
                seconds = int(current_shift['end'] - time())
                response['full_text'] = 'current shift ends in' + str(datetime.timedelta(seconds=seconds))
            elif next_shift:
                seconds = int(next_shift['start'] - time())
                response['full_text'] = 'next shift in ' + str(datetime.timedelta(seconds=seconds))
            else:
                response['full_text'] = 'Dobby is a free elf!'

        except:
            response['full_text'] = ''

        return response

if __name__ == "__main__":
    """
    Test this module by calling it directly.
    """
    from time import sleep
    x = Py3status()
    config = {
        'color_good': '#00FF00',
        'color_bad': '#FF0000',
    }
    while True:
        print(x.check([], config))
        sleep(1)
