import argparse
import os
from pathlib import Path

import make_fingerprint as mf
import data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='covert tracelog to wifi fingerprint csv')

    parser.add_argument('--trace-log', type=str,
                    help='<trace file name>')

    args = parser.parse_args()
    trace_log = args.trace_log

    for file_name in os.listdir(Path(trace_log)):
        log_file = f"{trace_log}/{file_name}"
        if log_file[-3:].lower() != "txt":
            continue

        fps, posis = mf.bind_wifi_fingerprints(
            mf.filtering(log_file))

        data.save_json(f"{log_file[:-4]}_fps.json", fps)
        data.save_json(f"{log_file[:-4]}_posis.json", posis)