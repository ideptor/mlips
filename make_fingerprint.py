
from typing import Tuple, List
from data import WifiFingerprint, POSI, WIFI

def filtering(trace_file_name: str, must_include_head: List[str]) -> List[str]:

    filtered_lines = []
    with open(trace_file_name, "r") as f:
        filtered_lines = []
        while True:
            line = f.readline()
            if not line: break
            for head in must_include_head:
                if head in line:
                    filtered_lines.append(line)
                    continue
    
    return filtered_lines



def bind_wifi_fingerprints(logs:str) -> \
        Tuple[List[WifiFingerprint], List[POSI]]:

    posis = []
    fps = []
    TIME_DURATION = 3
    cur_timestamp = 0
    
    cur_fp = WifiFingerprint.create(None)

    for log in logs:

        if "POSI;" in log[:5]:
            if len(cur_fp.wifi_dict.keys()) > 0:
                fps.append(cur_fp)
            posi = POSI.from_log(log)
            posis.append(posi)
            cur_timestamp = posi.timestamp

            cur_fp = WifiFingerprint.create(cur_timestamp)

        if "WIFI;" in log[:5]:
            wifi = WIFI.from_log(log)
            if (wifi.timestamp - cur_timestamp) > TIME_DURATION:
                fps.append(cur_fp)
                cur_timestamp = wifi.timestamp
                cur_fp = WifiFingerprint.create(cur_timestamp)
            cur_fp.add_wifi(wifi)

    if len(cur_fp.wifi_dict.keys()) > 0:
        fps.append(cur_fp)

    return (fps, posi)