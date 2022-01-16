import os
import pandas as pd

import data
import make_fingerprint as mf

def test_load_logfile():
    # given
    trace_file_name = "test/data/filtering_test.txt"
    #must_include_head = ["POSI;", "WIFI;", "MAGN;"]
    must_include_head = ["POSI;", "WIFI;"]

    # when
    filtered_lines = mf.load_logfile(trace_file_name, must_include_head)

    # then
    assert "ACCE;" not in filtered_lines[:100]
    assert len(filtered_lines) == 4


def test_bind_wifi_fingerprints():
    
    # given
    trace_file_name = "test/data/wifi_calibration.txt"
    must_include_head = ["POSI;", "WIFI;"]
    filtered_lines = mf.load_logfile(trace_file_name, must_include_head)

    # when
    fps, _ = mf.bind_wifi_fingerprints(filtered_lines)

    # then
    assert len(fps[0].wifi_dict) == 2
    assert fps[0].timestamp == 61.472
    assert fps[0].last_landmark == 1

    assert len(fps[1].wifi_dict) == 3
    assert fps[1].timestamp == 68.396
    assert fps[1].last_landmark == 1

    assert len(fps[2].wifi_dict) == 4
    assert fps[2].timestamp == 115.986
    assert fps[2].last_landmark == 2

    assert len(fps) == 3



def test_fill_latitude_longitude():

    # given

    posis = data.load_from_json_file(
        "test/data/test_posis.json", data.POSI
    )
    assert len(posis) == 4

    fps = data.load_from_json_file(
        "test/data/test_fps.json", data.WifiFingerprint
    )
    assert len(fps) == 50
    assert fps[0].latitude is None
    assert fps[0].longitude is None


    # when
    fps_new = mf.fill_latitude_longitude(fps, posis)

    # then
    assert fps_new[0].latitude is not None
    assert fps_new[0].longitude is not None


def test_save_fingerprint_as_csv():

    # given
    posis = data.load_from_json_file(
        "test/data/test_posis.json", data.POSI
    )
    assert len(posis) == 4

    fps = data.load_from_json_file(
        "test/data/test_fps.json", data.WifiFingerprint
    )
    assert len(fps) == 50
    fps = mf.fill_latitude_longitude(fps, posis)

    assert fps[0].latitude is not None
    assert fps[0].longitude is not None
    assert fps[0].region is None
    assert len(fps[0].wifi_dict.keys()) == 34
    assert str(list(fps[0].wifi_dict.values())[0]) == "WIFI(timestamp=64.373, sensor_timestamp=12313.167, ssid_name='SSID_0012', mac='20:19:00:00:00:53', freq=2412, rssi=-32)"

    fps = mf.bucketization(fps)
    assert fps[0].region is not None

    test_csv_file_name = "test.csv"
    if os.path.isfile(test_csv_file_name):
        os.remove(test_csv_file_name)
    assert os.path.isfile(test_csv_file_name) is False
    
    # when 
    data.save_fingerprint_as_csv(test_csv_file_name, fps)
    
    # then
    assert os.path.isfile(test_csv_file_name) is True

    df = pd.read_csv(test_csv_file_name)
    
    os.remove(test_csv_file_name)