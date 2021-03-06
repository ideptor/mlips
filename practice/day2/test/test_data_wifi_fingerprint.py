import json
import os

from data import WIFI, WifiFingerprint
import data
import make_fingerprint as mf

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


def test_wifi_from_dict():

    # given
    wifi_json_str = '{"timestamp": 64.373, "sensor_timestamp": 12313.167, "ssid_name": "SSID_0012", "mac": "20:19:00:00:00:53", "freq": 2412, "rssi": -32}'
    wifi_dict = json.loads(wifi_json_str)

    # when
    wifi = WIFI(**wifi_dict)

    # then
    assert type(wifi) is WIFI


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
    "last_landmark": 1,
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
    },
    "region": null,
    "latitude": null,
    "longitude": null
  }
]'''
    
    os.remove(fps_json_file_name)


def test_create_wifi_fingerprint_from_dict():

    # given
    json_file_name = "test/data/test_fingerprint.json"
    fp_dict = WifiFingerprint.from_json_file(json_file_name).dict()

    # when
    fp = WifiFingerprint.from_dict(fp_dict)

    # then
    assert fp is not None
    assert fp.wifi_cnt() == 38


def test_create_wifi_fingerprints_from_json_file():
    
    # given
    json_file_name = "test/data/test_fps.json"

    # when
    fps = data.load_from_json_file(json_file_name, WifiFingerprint) 

    # then
    assert fps is not None
    assert len(fps) == 50

