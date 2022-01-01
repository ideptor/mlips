import json
import os
from pathlib import Path

from data import POSI, WIFI
import data
import make_fingerprint as mf

def test_create_posi():

    # given
    log = "POSI;61.472;1;43.7182527866061;10.4215241271896;1;60"

    # when
    posi = POSI.from_log(log)

    # then
    assert posi.timestamp == 61.472
    assert posi.landmark == 1
    assert posi.latitude == 43.7182527866061
    assert posi.longitude == 10.4215241271896
    assert posi.floor_id == 1
    assert posi.bulding_id == 60


def test_create_posi_negative():

    # given
    log = "WIFI;64.373;12313.167;SSID_0012;20:19:00:00:00:53;2412;-32"

    # when
    posi = POSI.from_log(log)

    # then
    assert posi is None


def test_create_wifi():

    # given
    log = "WIFI;64.373;12313.167;SSID_0012;20:19:00:00:00:53;2412;-32"


    # when
    wifi = WIFI.from_log(log)

    # then
    assert wifi.timestamp == 64.373
    assert wifi.sensor_timestamp == 12313.167
    assert wifi.ssid_name == "SSID_0012"
    assert wifi.mac == "20:19:00:00:00:53"
    assert wifi.freq == 2412
    assert wifi.rssi == -32

def test_create_wifi_negative():

    # given
    log = "POSI;61.472;1;43.7182527866061;10.4215241271896;1;60"

    # when
    wifi = WIFI.from_log(log)

    # then
    assert wifi is None


def test_wifi_as_dict():

    # given
    log = "WIFI;64.373;12313.167;SSID_0012;20:19:00:00:00:53;2412;-32"
    
    # when
    wifi = WIFI.from_log(log)

    # then
    assert json.dumps(wifi.dict()) == '{"timestamp": 64.373, "sensor_timestamp": 12313.167, "ssid_name": "SSID_0012", "mac": "20:19:00:00:00:53", "freq": 2412, "rssi": -32}'

    
def test_posi_as_dict():

    # given
    log = "POSI;61.472;1;43.7182527866061;10.4215241271896;1;60"
    
    # when
    posi = POSI.from_log(log)

    # then
    assert json.dumps(posi.dict()) == '{"timestamp": 61.472, "landmark": 1, "latitude": 43.7182527866061, "longitude": 10.4215241271896, "floor_id": 1, "bulding_id": 60}'


def test_posi_save_json():

    # given
    log = "POSI;61.472;1;43.7182527866061;10.4215241271896;1;60"
    posi = POSI.from_log(log)
    posi_json_file_name = "test/data/test_generated_posi.json"
    try:
        os.remove(posi_json_file_name)
    except:
        pass
    assert os.path.isfile(posi_json_file_name) is False

    # when
    data.save_json(posi_json_file_name, [posi])

    #then
    assert os.path.isfile(posi_json_file_name)
    
    f = open(posi_json_file_name, "r")
    json_str = f.read()
    assert json_str == '''[
  {
    "timestamp": 61.472,
    "landmark": 1,
    "latitude": 43.7182527866061,
    "longitude": 10.4215241271896,
    "floor_id": 1,
    "bulding_id": 60
  }
]'''
    try:
        os.remove(posi_json_file_name)
    except:
        pass


def test_wifi_fingerprints_save_json():
    # given
    logs = '''
POSI;61.372;1;43.7182527866061;10.4215241271896;1;60
WIFI;64.373;12313.167;SSID_0012;20:19:00:00:00:53;2412;-32
WIFI;64.373;12313.167;SSID_0007;20:19:00:00:00:52;2412;-33
''' 
    fps_json_file_name = "test/data/test_generated_fps.json"
    try:
        os.remove(fps_json_file_name)
    except:
        pass
    assert os.path.isfile(fps_json_file_name) is False

    # when
    fps, _ = mf.bind_wifi_fingerprints(logs.split("\n"))
    data.save_json(fps_json_file_name, fps)

    #then
    assert os.path.isfile(fps_json_file_name)
    
    f = open(fps_json_file_name, "r")
    json_str = f.read()
    assert json_str == '''[
  {
    "timestamp": 64.373,
    "wifi_dict": {
      "20:19:00:00:00:53": {
        "timestamp": 64.373,
        "sensor_timestamp": 12313.167,
        "ssid_name": "SSID_0012",
        "mac": "20:19:00:00:00:53",
        "freq": 2412,
        "rssi": -32
      },
      "20:19:00:00:00:52": {
        "timestamp": 64.373,
        "sensor_timestamp": 12313.167,
        "ssid_name": "SSID_0007",
        "mac": "20:19:00:00:00:52",
        "freq": 2412,
        "rssi": -33
      }
    }
  }
]'''
    
    try:
        os.remove(fps_json_file_name)
    except:
        pass

    