
from typing import Tuple, List
from data import WifiFingerprint, POSI, WIFI

def filtering(trace_file_name: str, 
            must_include_head: List[str] =["WIFI;", "POSI;"]) \
                -> List[str]:

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



def bind_wifi_fingerprints(logs:List[str]) -> \
        Tuple[List[WifiFingerprint], List[POSI]]:

    posis = []
    fps = []
    TIME_DURATION = 3
    cur_timestamp = 0.
    cur_landmark = None
    
    cur_fp = WifiFingerprint.create()

    for log in logs:

        if "POSI;" in log[:5]:
            if cur_fp.wifi_cnt() > 0:
                fps.append(cur_fp)
            posi = POSI.from_log(log)
            posis.append(posi)
            cur_timestamp = posi.timestamp
            cur_landmark = posi.landmark

            cur_fp = WifiFingerprint.create(cur_timestamp, cur_landmark)

        if "WIFI;" in log[:5]:
            wifi = WIFI.from_log(log)
            if (wifi.timestamp - cur_timestamp) > TIME_DURATION:
                if cur_fp.wifi_cnt() > 0:
                    fps.append(cur_fp)
                cur_timestamp = wifi.timestamp
                cur_fp = WifiFingerprint.create(cur_timestamp, cur_landmark)
            cur_fp.add_wifi(wifi)

    if len(cur_fp.wifi_dict.keys()) > 0:
        fps.append(cur_fp)

    return (fps, posis)