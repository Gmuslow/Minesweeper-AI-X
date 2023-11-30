# Minesweeper-AI-X
A machine-learning-based MineSweeper AI that can solve a set of bomb functions.

To run the Python model:
pip install gym

To train the q-table, run:
python agent/evaluator.py train BOARD_SIZE

where BOARD_SIZE represents the dimensions of the board (ONLY WORKS ON SQUARE BOARDS)

To return an action corresponding to a state, run:
python agent/evaluator.py test BOARD_SIZE

This will print out the square that the model decided to click on.

Board indices below:
  0  1   2
0[x ,x ,x ]
1[x, x, x ]
2[x, x, x ]

Coordinate (2, 2) represents the lower right corner.
