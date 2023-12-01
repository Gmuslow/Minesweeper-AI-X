import argparse
from peaceful_pie.unity_comms import UnityComms

def run(args: argparse.Namespace) -> None:
    unity_comms = UnityComms(port=args.port)
    unity_comms.RevealCell(x=args.x,y=args.y)
    """ Does essentially what a user does when clicking a square, using parameters
        for position."""
    print('done')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--x', type=int, required=True)
    parser.add_argument('--y', type=int, required=True)
    parser.add_argument('--port', type=int, default=9000)
    args = parser.parse_args()
    run(args)