
from collections import defaultdict
from typing import Tuple, List
import copy

from data import WifiFingerprint, POSI, WIFI

def load_logfile(trace_file_name: str, 
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


def fill_latitude_longitude(
    fps:List[WifiFingerprint], 
    posis:List[POSI], 
    exclude_landmark = [None, 2,4]) -> List[WifiFingerprint]:

    posi_dict = dict(zip([p.landmark for p in posis], posis))
    
    landmark_fps_dict = defaultdict(lambda: list())
    for fp in fps:
        if fp.last_landmark not in exclude_landmark:
            landmark_fps_dict[fp.last_landmark].append(copy.deepcopy(fp))

    fps_new = []
    for landmark, fps in landmark_fps_dict.items():

        start = posi_dict[landmark]
        end = posi_dict[landmark+1]

        latitude_unit = (end.latitude - start.latitude) / len(fps)
        longitude_unit = (end.longitude - start.longitude) / len(fps)
        
        for idx, fp in enumerate(fps):
            fp.latitude = start.latitude + (idx+1) * latitude_unit
            fp.longitude = start.longitude + (idx+1) * longitude_unit
            #print(f"{fp.last_landmark} / {fp.latitude:10.7f}, {fp.longitude:10.7f}")
            fps_new.append(fp)
 
    return fps_new