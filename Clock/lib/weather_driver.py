#! /usr/bin/env python

import json
import random
import requests


class WeatherDriver(object):
    def __init__(self, ApiKeys, Config):
        self.wuapi_key = ""
        self.dsapi_key = ""
        if ApiKeys.wuapi:
            self.wuapi_key = ApiKeys.wuapi
        if ApiKeys.dsapi:
            self.dsapi_key = ApiKeys.dsapi
        self.config = Config

    def get_keys(self):
        return self.wuapi_key, self.dsapi_key

    def update_data():
        pass

    def get_current(self):
        if len(self.wuapi_key) > 0:
            self._get_wunderground()
        return self.current

    def _set_wunderground_url(self):
        build_str = []
        build_str.append(self.config.wuprefix)
        build_str.append(self.wuapi_key)
        build_str.append('/conditions/astronomy/')
        build_str.append('hourly10day/forecast10day/lang:')
        build_str.append(self.config.wuLanguage + '/q/')
        build_str.append(str(self.config.wulocation.lat) + ',')
        build_str.append(str(self.config.wulocation.lng) + '.json')
        build_str.append('?r=' + str(random.random()))
        self.wxurl = ''.join(build_str)

    def _get_wxurl(self):
        if "wxurl" not in self.get_keys():
            self._set_wunderground_url()
        return self.wxurl

    def _get_wunderground(self):
        if "wxurl" not in self.get_keys():
            self._set_wunderground_url()
        self.wunderground = None
        try:
            self.wunderground = requests.get(self.wxurl)
        except:
            pass

        current = self.wunderground.json()["current_observation"]
        self.return_data = {
            "current_observation": {
                "icon_url": current["icon_url"],
                "weather": current["weather"],
                "pressure_trend": current["pressure_trend"],
                "relative_humidity": current["relative_humidity"],
                "wind_dir": current["wind_dir"],
                "local_epoch": current["local_epoch"]
            }
        }
        if self.config.metric:
            self.return_data["current_observation"]["temp"] =\
                current["temp_c"]
            self.return_data["current_observation"]["pressure"] =\
                current["pressure_mb"]
            self.return_data["current_observation"]["wind"] =\
                current["wind_kph"]
            self.return_data["current_observation"]["wind_gust"] =\
                current["wind_gust_kph"]
            self.return_data["current_observation"]["precip_1hr"] =\
                current["precip_1hr_metric"]
            self.return_data["current_observation"]["precip_today"] =\
                current["precip_today_metric"]
            self.return_data["current_observation"]["feels_like"] =\
                current["feelslike_c"]
        else:
            self.return_data["current_observation"]["temp"] =\
                current["temp_f"]
            self.return_data["current_observation"]["pressure"] =\
                current["pressure_in"]
            self.return_data["current_observation"]["wind"] =\
                current["wind_mph"]
            self.return_data["current_observation"]["wind_gust"] =\
                current["wind_gust_mph"]
            self.return_data["current_observation"]["precip_1hr"] =\
                current["precip_1hr_in"]
            self.return_data["current_observation"]["precip_today"] =\
                current["precip_today_in"]
            self.return_data["current_observation"]["feels_like"] =\
                current["feelslike_f"]
        del current

        self.return_data["sun_phase"] =\
            self.wunderground.json()["sun_phase"]
        self.return_data["moon_phase"] =\
            self.wunderground.json()["moon_phase"]

        hourly = self.wunderground.json()["hourly_forecast"]
        self.return_data['hourly_forecast'] = []
        for i in range(0, 3):
            self.return_data['hourly_forecast'].append(hourly[i*3+2])

        simpleforecast = self.wunderground.json()["forecast"]["simpleforecast"]
        del self.wunderground

        self.return_data["forecast"] =\
            json.loads('{"simpleforecast": {"forecastday": []}}')

        for i in range(0, 6):
            self.return_data["forecast"]["simpleforecast"]["forecastday"].\
                append(simpleforecast["forecastday"][i])

        del simpleforecast
        self.current = self.return_data
        del self.return_data

    def _get_darksky(self):
        build_str = []
        build_str.append[self.config.dsurl]
        build_str.append[self.config.dsapi_key]
        build_str.append[self.config.wulocation.lat + ',']
        build_str.append[self.config.wulocation.lon]
        self.dsurl = ''.join(build_str)

        self.darksky = None

        try:
            self.darksky = requests.get(self.dsurl)
        except:
            pass

        if len(self.darksky.items()) > 0:
            pass
        else:
            self.darksky = None

    def _standardize_ds(self):
        pass
