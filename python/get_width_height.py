import argparse
from peaceful_pie.unity_comms import UnityComms

def run(args: argparse.Namespace) -> None:
    unity_comms = UnityComms(port=args.port)
    result = unity_comms.GetWidthHeight()
    print('result', result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=9000)
    args = parser.parse_args()
    run(args)