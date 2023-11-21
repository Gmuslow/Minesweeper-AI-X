
import numpy as np
import gym
from gym import spaces
from gym.envs.registration import register


# default : easy board
BOARD_SIZE = 5
NUM_MINES = 3

# cell values, non-negatives indicate number of neighboring mines
MINE = -1
CLOSED = -2

def is_new_move(my_board, x, y):
    """ return true if this is not an already clicked place"""
    return my_board[x, y] == CLOSED


def is_valid(x, y):
    """ returns if the coordinate is valid"""
    return (x >= 0) & (x < BOARD_SIZE) & (y >= 0) & (y < BOARD_SIZE)


def is_win(my_board):
    """ return if the game is won """
    return np.count_nonzero(my_board == CLOSED) == NUM_MINES


def is_mine(board, x, y):
    """return if the coordinate has a mine or not"""
    return board[x, y] == MINE


class MinesweeperEnv(gym.Env):
    
    def __init__(self, board_size=BOARD_SIZE, num_mines=NUM_MINES):
        """
        Create a minesweeper game.

        Parameters
        ----
        board_size: int     shape of the board
            - int: the same as (int, int)
        num_mines: int   num mines on board
        """

        self.board_size = board_size
        self.num_mines = num_mines
        self.board = CreateMineField(board_size, num_mines)
        self.my_board = np.ones((board_size, board_size), dtype=int) * CLOSED
        self.num_actions = 0

        self.observation_space = spaces.Box(low=-2, high=9,
                                            shape=(self.board_size, self.board_size))
        self.action_space = spaces.Discrete(self.board_size*self.board_size)
        self.valid_actions = np.ones((self.board_size * self.board_size), dtype=bool)

    def count_neighbour_mines(self, x, y):
        """return number of mines in neighbour cells given an x-y coordinate

            Cell -->Current Cell(row, col)
            N -->  North(row - 1, col)
            S -->  South(row + 1, col)
            E -->  East(row, col + 1)
            W -->  West(row, col - 1)
            N.E --> North - East(row - 1, col + 1)
            N.W --> North - West(row - 1, col - 1)
            S.E --> South - East(row + 1, col + 1)
            S.W --> South - West(row + 1, col - 1)
        """
        neighbour_mines = 0
        for _x in range(x - 1, x + 2):
            for _y in range(y - 1, y + 2):
                if is_valid(_x, _y):
                    if is_mine(self.board, _x, _y):
                        neighbour_mines += 1
        return neighbour_mines

    def open_neighbour_cells(self, my_board, x, y):
        """return number of mines in neighbour cells given an x-y coordinate

            Cell -->Current Cell(row, col)
            N -->  North(row - 1, col)
            S -->  South(row + 1, col)
            E -->  East(row, col + 1)
            W -->  West(row, col - 1)
            N.E --> North - East(row - 1, col + 1)
            N.W --> North - West(row - 1, col - 1)
            S.E --> South - East(row + 1, col + 1)
            S.W --> South - West(row + 1, col - 1)
        """
        for _x in range(x-1, x+2):
            for _y in range(y-1, y+2):
                if is_valid(_x, _y):
                    if is_new_move(my_board, _x, _y):
                        my_board[_x, _y] = self.count_neighbour_mines(_x, _y)
                        if my_board[_x, _y] == 0:
                            my_board = self.open_neighbour_cells(my_board, _x, _y)
        return my_board

    def get_next_state(self, state, x, y):
        
        my_board = state
        game_over = False
        if is_mine(self.board, x, y):
            my_board[x, y] = MINE
            game_over = True
        else:
            my_board[x, y] = self.count_neighbour_mines(x, y)
            if my_board[x, y] == 0:
                my_board = self.open_neighbour_cells(my_board, x, y)
        self.my_board = my_board
        return my_board, game_over

    def reset(self):
        self.my_board = np.ones((self.board_size, self.board_size), dtype=int) * CLOSED
        self.board = CreateMineField(self.board_size, self.num_mines)
        self.num_actions = 0
        self.valid_actions = np.ones((self.board_size * self.board_size), dtype=bool)

        return self.my_board

    def step(self, action, debug=False):
        
        state = self.my_board
        x  = action[0]
        y = action[1]

        next_state, reward, done, info = self.next_step(state, x, y, debug)
        self.my_board = next_state
        self.num_actions += 1
        self.valid_actions = (next_state.flatten() == CLOSED)
        info['valid_actions'] = self.valid_actions
        info['num_actions'] = self.num_actions
        return next_state, reward, done, info

    def next_step(self, state, x, y, wait=False):
        my_board = state
        if not is_new_move(my_board, x, y):
            if wait:
                print("Reward: 0")
            return my_board, -1, False, {}
        while True:
            state, game_over = self.get_next_state(my_board, x, y)
            if not game_over:
                if is_win(state):
                    if wait:
                        print("You Win!")
                    return state, 10, True, {}
                else:
                    if wait:
                        print("Reward: 1")
                    return state, 1, False, {}
            else:
                return state, -5, True, {}

    def render(self, mode='human'):
            return 0
    def get_Q(self): #create initial Q table
        num_states = (self.board_size ** 2, self.board_size ** 2)
        num_actions = self.board_size * self.board_size
        q_table = np.zeros((num_states[0], num_states[1], num_actions))
        print(q_table)
        return q_table

import random
# def CreateMineField(x, y, numBombs):
#     grid = [[0 for _ in range(x)] for _ in range(y)]

#     # Place bombs
#     print(grid)
#     for i in range(numBombs):
#         bomb = [random.randint(0, x - 2), random.randint(0, y - 2)]
#         print(bomb)
#         grid[bomb[0]][bomb[1]] = -1

#     for i in range(x):
#         for j in range(y):
#             if grid[i][j] == -1:
#                 continue
#             count = 0
#             left = i - 1 >= 0
#             right = i + 1 < x
#             top = j + 1 < y
#             bottom = j - 1 >= 0

#             if left and bottom:
#                 if grid[i - 1][j - 1] == -1:
#                     count+=1
#             if left:
#                 if grid[i - 1][j] == -1:
#                     count+=1
#             if left and top:
#                 if grid[i - 1][j + 1] == -1:
#                     count+=1
#             if top:
#                 if grid[i][j + 1] == -1:
#                     count+=1
#             if top and right:
#                 if grid[i + 1][j + 1] == -1:
#                     count+=1
#             if right:
#                 if grid[i + 1][j] == -1:
#                     count+=1
#             if right and bottom:
#                 if grid[i + 1][j - 1] == -1:
#                     count+=1
#             if bottom:
#                 if grid[i][j - 1] == -1:
#                     count+=1
            
#             grid[i][j] = count
    #print(grid)
    # for r in range(len(grid)):
    #     print(grid[len(grid) - r - 1])




def CreateMineField(board_size, num_mines):
    """generate a board, place mines randomly"""
    mines_placed = 0
    board = np.zeros((board_size, board_size), dtype=int)
    while mines_placed < num_mines:
        rnd = np.random.randint(0, board_size * board_size)
        x = int(rnd / board_size)
        y = int(rnd % board_size)
        if is_valid(x, y):
            if not is_mine(board, x, y):
                board[x, y] = MINE
                mines_placed += 1
    return board


class QTable:
    def __init__(self, board_size, learning_rate, discount_factor):
        self.q_table = {}
        self.board_size = board_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

    def get_q_values(self, state):
        state_key = str(state)
        if state_key not in self.q_table:
            # Initialize Q-values for each action
            self.q_table[state_key] = np.zeros(self.board_size ** 2)  # num_actions is the number of possible actions

        return self.q_table[state_key]

    def update_q_values(self, state, action, next_state, reward, debug=False): #actions come in the form (x, y)
        currentActionIndex = action[0] + self.board_size * action[1]
        next_q_values = self.get_q_values(next_state)
        best_next_action = np.argmax(next_q_values)
        current_q_values = self.get_q_values(state)
        self.q_table[str(state)][currentActionIndex] += self.learning_rate * (
            reward + discount_factor * self.q_table[str(next_state)][best_next_action] - self.q_table[str(state)][currentActionIndex]
        )
        if debug:
            print(self.q_table)



def epsilon_greedy_policy(q_values, epsilon):
    """
    Epsilon-greedy policy for selecting an action.

    Parameters:
    - state: Current state of the environment
    - q_values: Q-values for the current state
    - epsilon: Probability of choosing a random action (exploration)

    Returns:
    - selected_action: The selected action
    """

    if np.random.rand() < epsilon:
        # Explore: choose a random action
        selected_action = np.random.randint(len(q_values))
    else:
        # Exploit: choose the action with the highest Q-value
        selected_action = np.argmax(q_values)

    return selected_action


def StringifyState(state):
    return str(state)

import os
import time
if __name__ == "__main__":
    env = MinesweeperEnv()
    
    learning_rate = 0.1
    discount_factor = 0.9
    num_episodes = 10000
    epsilon = 0.1
    q_table = QTable(env.board_size, learning_rate, discount_factor)

    visual = True
    delay = 0.2
    cutoff = num_episodes - 50
    for episode in range(num_episodes):
        state = env.reset()
        
        done = False
        max_steps = 100
        while not done and max_steps > 0:
            # Choose action using epsilon-greedy strategy
            action = epsilon_greedy_policy(q_table.get_q_values(state), epsilon)
            placeToClick = (action % BOARD_SIZE, int(action / BOARD_SIZE))
            # Take action and observe next state and reward
            next_state, reward, done, _ = env.step(placeToClick, episode > cutoff)
            
            # Update Q-values
            q_table.update_q_values(state, placeToClick, next_state, reward)

            # Update state
            state = next_state
            
            if visual and episode > cutoff:
                os.system("cls")
                print(state)
                print("\n")
                if done:
                    print("Game Over")
                    time.sleep(1) 
                time.sleep(delay)
            max_steps -=1
    