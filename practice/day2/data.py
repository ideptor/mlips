
from typing import Dict, List, Union
from dataclasses import asdict, dataclass
import json
import pandas as pd
import os

@dataclass
class POSI:
    #POSI;Timestamp(s);Landmark;Latitude(degrees);Longitude(degrees);floor ID(0,1,2..4);Building ID(0,1,2..3)
    
    timestamp: float
    landmark: int
    latitude: float
    longitude: float
    floor_id: int
    bulding_id: int
        
    def dict(self):
        return asdict(self)

    @staticmethod
    def from_log(log:str):
        tokens = log.strip().split(";")
        if tokens[0] != "POSI":
            return None

        posi = POSI(
            float(tokens[1]),
            int(tokens[2]),
            float(tokens[3]),
            float(tokens[4]),
            int(tokens[5]),
            int(tokens[6])
        )
        return posi

    
    @staticmethod
    def from_json_file(json_file_name:str):
        with open(json_file_name, "r") as f:
            posi_dict = json.load(f)
            return POSI.from_dict(posi_dict)
    
    @staticmethod
    def from_dict(posi_dict: dict):
        return POSI(**posi_dict)

@dataclass
class WIFI:
    #WIFI;AppTimestamp(s);SensorTimeStamp(s);Name_SSID;MAC_BSSID;Frequency(Hz);RSS(dBm)
    
    timestamp: float
    sensor_timestamp: float
    ssid_name: str
    mac: str
    freq: int
    rssi: int

    def dict(self):
        return asdict(self)

    @staticmethod
    def from_log(log:str):
        tokens = log.strip().split(";")
        if tokens[0] != "WIFI":
            return None

        wifi = WIFI(
            float(tokens[1]),
            float(tokens[2]),
            str(tokens[3]).strip(),
            str(tokens[4]).strip(),
            int(tokens[5]),
            int(tokens[6])
        )
        return wifi

    @staticmethod
    def from_dict(wifi_dict: dict):
        return WIFI(**wifi_dict)


@dataclass
class WifiFingerprint:

    timestamp: float
    last_landmark: int
    wifi_dict: Dict[str, WIFI]
    region: int = None
    latitude: float = None
    longitude: float = None
    
    def add_wifi(self, wifi:WIFI):
        self.wifi_dict[wifi.mac] = wifi

    def wifi_cnt(self):
        return len(self.wifi_dict)

    def dict(self):
        return asdict(self)

    @staticmethod
    def create(timestamp: float=None, last_landmark=None):
        fp = WifiFingerprint(
            timestamp,
            last_landmark,
            dict()
        )
        return fp

    
    @staticmethod
    def from_json_file(json_file_name:str):
        with open(json_file_name, "r") as f:
            fp_dict = json.load(f)
            return WifiFingerprint.from_dict(fp_dict)

    @staticmethod
    def from_dict(fp_dict: dict):
        fp = WifiFingerprint(**fp_dict)
        wifi_dict = {}
        for w, v in fp_dict['wifi_dict'].items():
            wifi_dict[w] = WIFI.from_dict(v)
        fp.wifi_dict = wifi_dict
        return fp
    

def save_json(file_name: str,
        collection: List[Union[POSI, WifiFingerprint]]):
    
    json_list = []
    for item in collection:
        json_list.append(item.dict())
    
    f = open(file_name, "w")
    f.write(json.dumps(json_list, indent=2))
    print(f'"{file_name}" has been created.')


def load_from_json_file(file_name:str, data_class: Union[POSI, WifiFingerprint]) -> List:
    with open(file_name, "r") as f:
        dict_list = json.load(f)

    collection = []
    for item in dict_list:
        collection.append(data_class.from_dict(item))

    return collection   


def save_fingerprint_as_csv(file_name: str, fps: List[WifiFingerprint]):
    mac_set = set()
    for fp in fps:
        for mac in fp.wifi_dict.keys():
            mac_set.add(mac)

    columns = ['timestamp', 'region', 'latitude', 'longitude']
    columns.extend(list(mac_set))
    
    data = []
    for fp in fps:
        row = [fp.timestamp, fp.region, fp.latitude, fp.longitude]
        for mac in mac_set:
            if mac in fp.wifi_dict.keys():
                row.append(fp.wifi_dict[mac].rssi)
            else:
                row.append(None)
                
        data.append(row)
        
    data_frame = pd.DataFrame(data, columns=columns)
    data_frame.to_csv(file_name, index=False)
    print(f"exported: {os.path.abspath(file_name)}")