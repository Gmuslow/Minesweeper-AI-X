import argparse
from peaceful_pie.unity_comms import UnityComms

def run(args: argparse.Namespace) -> None:
    unity_comms = UnityComms(port=args.port)
    result = unity_comms.GameActive()
    with open('game_active.txt', 'w') as f:
        if result:
            f.write("true")
        else:
            f.write("false")
        f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=9000)
    args = parser.parse_args()
    run(args)