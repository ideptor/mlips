import argparse
import make_fingerprint as mf

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='covert tracelog to wifi fingerprint csv')

    parser.add_argument('--trace-log', type=str,
                    help='<trace file name>')

    args = parser.parse_args()
    trace_log = args.trace_log

    fps, posis = mf.bind_wifi_fingerprints(
        mf.filtering(args.trace_log))

    posis.save_as_json(f"{trace_log[:-3]}_posis.json")