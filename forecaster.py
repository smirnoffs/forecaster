import json
import time

import requests

import settings


def build_url(lat, lng, time_stamp=None):
    mask = 'https://api.darksky.net/forecast/{key}/{latitude},{longitude}'
    if time_stamp:
        mask += ',{time}'
    key = settings.SECRET_KEY
    return mask.format(key=key, latitude=lat, longitude=lng, time=time_stamp)


def get_forecast(lat, lng):
    url = build_url(lat, lng)
    response = requests.get(url, params={'lang': settings.LANG, 'units': 'si'})
    content = response.content.decode('utf-8')
    if response.status_code != 200:
        print(content)
    decoded_response = json.loads(content)
    summary_hourly = decoded_response['hourly']['summary']
    next_hour = decoded_response['hourly']['data'][1]
    next_hour_temperature = next_hour['temperature']
    next_hour_precipitation_type = next_hour.get('precipType')
    next_hour_precipitation_probability = next_hour['precipProbability']
    return next_hour_temperature, next_hour_precipitation_type, next_hour_precipitation_probability, summary_hourly


def get_time_machine(lat, lng):
    time_24_hours_ago = int(time.time()) - 24 * 60 * 60
    url = build_url(lat, lng, time_24_hours_ago)
    response = requests.get(url, params={'lang': settings.LANG, 'units': 'si',
                                         'exclude': 'minutely,hourly,daily,alerts,flags'})
    decoded_response = json.loads(response.content.decode('utf-8'))
    temperature = decoded_response['currently']['temperature']
    return temperature


if __name__ == '__main__':
    BERLIN = ('52.531039', '13.348029')
    temperature, precipitation_type, precipitation_probability, summary_hourly = get_forecast(*BERLIN)
    historic_temperature = get_time_machine(*BERLIN)
    precipitation = ', {} ({}%)'.format(precipitation_type,
                                        int(precipitation_probability * 100)) if precipitation_type else ''
    message = '{}℃ (вчора було {}℃){}. {}'.format(temperature, historic_temperature, precipitation, summary_hourly)
    print(message)
    pushover_response = requests.post('https://api.pushover.net/1/messages.json',
                                      data={'token': settings.PUSHOVER_TOKEN,
                                            'user': settings.PUSHOVER_KEY,
                                            'message': message})
    print(pushover_response.content)
