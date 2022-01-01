
from dataclasses import dataclass

@dataclass
class POSI:
    #POSI;Timestamp(s);Landmark;Latitude(degrees);Longitude(degrees);floor ID(0,1,2..4);Building ID(0,1,2..3)
    
    timestamp: float
    landmark: int
    latitude: float
    longitude: float
    floor_id: int
    bulding_id: int

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

    @staticmethod
    def from_log(log:str):
        tokens = log.strip().split(";")
        if tokens[0] != "WIFI":
            return None

        wifi = WIFI(
            float(tokens[1]),
            float(tokens[2]),
            str(tokens[3]),
            str(tokens[4]),
            int(tokens[5]),
            int(tokens[6])
        )
        return wifi