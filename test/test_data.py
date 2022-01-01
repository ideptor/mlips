from data import POSI, WIFI

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