from nose.tools import assert_is_not_none, assert_equal
from mock import patch, MagicMock

from lib.weather_driver import WeatherDriver
import json
import ApiKeys
import Config


class TestForecast(object):
    @classmethod
    def setup_class(cls):
        cls.mock_get_patcher = patch('lib.weather_driver.requests.get')
        cls.mock_get = cls.mock_get_patcher.start()
        cls.test_driver = WeatherDriver(ApiKeys, Config)

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()
        pass

    def test_key_import(cls):
        test_driver = WeatherDriver(ApiKeys, Config)
        assert_is_not_none(test_driver.get_keys())

    def test_wxurl_build(cls):
        assert_is_not_none(cls.test_driver._get_wxurl())

    def test_wxurl_length_greater_than_20(cls):
        assert(len(cls.test_driver._get_wxurl()) > 20)

    def test_key_missing(cls):
        fake_apikeys = MagicMock()
        fake_apikeys.wuapi = "fake_key"
        test_driver = WeatherDriver(fake_apikeys, Config)
        assert_is_not_none(test_driver.get_keys())

    def test_expected_return_data(cls):
        sample_data = open('tests/files/conditons.1475188978.out').read()
        cls.mock_get.return_value.json.return_value = json.loads(sample_data)
        assert(json.loads(sample_data)["current_observation"]
               ["observation_time"] ==
               "Last Updated on September 29, 5:42 PM CDT")

    def test_wunderground_return(cls):
        sample_data = open('tests/files/conditons.1475188978.out').read()
        cls.mock_get.return_value.json.return_value = json.loads(sample_data)
        assert_is_not_none(cls.test_driver.get_current())
    
    def test_keys_included(cls):
        keys_list = ["sun_phase", "hourly_forecast", "current_observation",
            "forecast", "moon_phase"]
        assert_equal(keys_list, cls.test_driver.get_current().keys())

    def test_data_return_consistent(cls):
        # grab forecastio data and wunderground
        # ensure consistent return
        pass
