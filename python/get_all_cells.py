import argparse
import json
from peaceful_pie.unity_comms import UnityComms

def run(args: argparse.Namespace) -> None:
    unity_comms = UnityComms(port=args.port)
    result = unity_comms.GetAllCells()
    results = result.split("\n")
    data = dict()
    count = -1
    for x in results:
        count = count + 1
        if count != 0:
            intnums = []
            strnums = x.split(" ")
            for y in strnums:
                if y != '':{
                    intnums.append(int(y))
                }
            data[f'row_{count}'] = intnums 
    with open('state.json','w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=9000)
    args = parser.parse_args()
    run(args)