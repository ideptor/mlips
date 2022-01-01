
from typing import Dict, List, Union
from dataclasses import asdict, dataclass
import json

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


@dataclass
class WifiFingerprint:

    timestamp: float
    wifi_dict: Dict[str, WIFI]

    def add_wifi(self, wifi:WIFI):
        self.wifi_dict[wifi.mac] = wifi

    def wifi_cnt(self):
        return len(self.wifi_dict)

    def dict(self):
        return asdict(self)

    @staticmethod
    def create(timestamp: float):
        fp = WifiFingerprint(
            timestamp,
            dict()
        )
        return fp

def save_json(file_name: str,
        collection: List[Union[POSI, WifiFingerprint]]):
    
    json_list = []
    for item in collection:
        json_list.append(item.dict())
    
    f = open(file_name, "w")
    f.write(json.dumps(json_list, indent=2))
    print(f'"{file_name}" has been created.')
    