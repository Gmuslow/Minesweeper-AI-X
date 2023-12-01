import argparse
from peaceful_pie.unity_comms import UnityComms

def run(args: argparse.Namespace) -> None:
    unity_comms = UnityComms(port=args.port)
    result = unity_comms.IsCellRevealed(x=args.x,y=args.y)
    print('result', result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--x', type=int, required=True)
    parser.add_argument('--y', type=int, required=True)
    parser.add_argument('--port', type=int, default=9000)
    args = parser.parse_args()
    run(args)