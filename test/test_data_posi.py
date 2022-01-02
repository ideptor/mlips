import json
import os

from data import POSI
import data


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
    
    os.remove(posi_json_file_name)


def test_create_posi_negative():

    # given
    log = "WIFI;64.373;12313.167;SSID_0012;20:19:00:00:00:53;2412;-32"

    # when
    posi = POSI.from_log(log)

    # then
    assert posi is None


def test_create_posi_from_dict():

    # given
    json_file_name = "test/data/test_posi.json"
    posi_dict = POSI.from_json_file(json_file_name).dict()

    # when
    posi = POSI.from_dict(posi_dict)

    # then
    assert posi is not None
    assert posi.landmark == 4



def test_create_posi_from_json_file():

    # given
    json_file_name = "test/data/test_posi.json"

    # when
    posi = POSI.from_json_file(json_file_name)

    # then
    assert posi is not None
    assert posi.landmark == 4


def test_create_posis_from_json_file():
    
    # given
    json_file_name = "test/data/test_posis.json"

    # when
    #posis = data.load_posis_from_json_file(json_file_name)
    posis = data.load_from_json_file(json_file_name, POSI) 

    # then
    assert posis is not None
    assert len(posis) == 4