import json

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



def test_fill_lat_long():

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
