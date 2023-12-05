# Minesweeper-AI-X
A machine-learning-based MineSweeper AI that can solve a set of bomb functions.

To run the Python model:
pip install gym

To run Python to Unity communication:
pip install peaceful-pie

To train the q-table, run:
python agent/evaluator.py train BOARD_SIZE NUM_BOMBS

where BOARD_SIZE represents the dimensions of the board (ONLY WORKS ON SQUARE BOARDS)

To return an action corresponding to a state, run:
python agent/evaluator.py test BOARD_SIZE NUM_BOMBS

This will print out the square that the model decided to click on to the file result.txt

The program searches for an agent/state.json file that contains the board information.
The format of the state.json file is below:
{
    "row_1" : [0, 0, 0],
    "row_2" : [1, 1, 1],
    "row_3" : [-2, -2, -2]
}

Board indices below:
  0  1   2
0[x ,x ,x ]
1[x, x, x ]
2[x, x, x ]

Coordinate (2, 2) represents the lower right corner.

To have the AI play the Unity game:
First, open the Unity game.
Second, navigate to the python directory in command prompt and run "python play_game.py"
Third, the AI should play the Unity game automatically! Make sure the width/height and mine count are
parameters the AI has trained on. To stop it, you can ctrl+C on command prompt.
