import argparse
from peaceful_pie.unity_comms import UnityComms

def run(args: argparse.Namespace) -> None:
    unity_comms = UnityComms(port=args.port)
    result = unity_comms.GetCell(x=args.x,y=args.y)
    """ This function gets the current state of the cell on the board.
        If the number is 0, the cell is Empty, or has no mines around it.
        If the number is above 0, the cell is a Number, and has that many mines around it.
        If the number is -1, the cell is not revealed.
        If the number is -2, the cell is a revealed mine, and the game should be over.
        If the number is -3, there was an error in getting the cell, 
        which should never occur. """
    print('result', result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--x', type=int, required=True)
    parser.add_argument('--y', type=int, required=True)
    parser.add_argument('--port', type=int, default=9000)
    args = parser.parse_args()
    run(args)