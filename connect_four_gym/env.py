from gym import Env
from gym.spaces import Discrete, Dict, Tuple, Box
import numpy as np
import random
from datetime import datetime
import logging


NOW = datetime.now()
NOW = NOW.strftime("%m-%d-%Y   %H %M %S")


logging.basicConfig(filename = f'logs/py_logs/c4gym_log {NOW}.log', level = logging.DEBUG)
NUM_LOCS = 42
NUM_ROWS = 7

COLOR_MAP = {0: ' ', 1: 'Yellow', 2: 'Red'}
YELLOW_REWARD = 1
RED_REWARD = -1
NO_REWARD = 0

WINDOW_LENGTH = 4

END_C = '\033[0m'
RED_C= '\033[91m'
YELLOW_C= '\033[93m'

USE_COLOR = {'Yellow': YELLOW_C, 'Red': RED_C, ' ': ''}

def to_color(code):
    return COLOR_MAP[code]
def to_code(color):
    return 1 if color == 'O' else 2

def next_color(color):
    return 'X' if color == 'O' else 'O'

def agent_by_color(agents, color):
    for agent in agents:
        if agent.color == color:
            return agent



def after_action_state(state, action):
    board, color = state
    action = get_dropped_loc(board, action)
    nboard = list(board[:])
    nboard[action] = to_code(color)
    nboard = tuple(nboard)
    return nboard, next_color(color)


def check_game_status(board):

    for color_code in [1, 2]:
        for col in range(0, 42, 7): # check rows by looking through each column
            left_most = col + 4
            for i in range(col, left_most):
                if board[i : i+4] == [color_code] * WINDOW_LENGTH:
                    return color_code

        for row in range(0, 7): # check columns by looking through each row
            for j in range(row, row+21, 7):
                if [board[j], board[j+7], board[j + 14], board[j+21]] == [color_code] * WINDOW_LENGTH:
                    return color_code

        for piece in range(42): # check diagonals using integer div. and mod.
            LEFT = False
            RIGHT = False
            UP = False
            DOWN = False

            if piece // 7 in [0,1,2]: # check if 4 spaces are available in each direction
                DOWN = True
            if piece // 7 in [3,4,5]:
                UP = True

            if piece % 7 in [0,1,2,3]:
                RIGHT = True
            if piece % 7 in [3,4,5,6]:
                LEFT = True

            if RIGHT and UP:
                if [board[piece], board[piece - 6], board[piece - 12], board[piece - 18]] == [color_code] * 4:
                    return color_code
            if RIGHT and DOWN:
                if [board[piece], board[piece + 8], board[piece + 16], board[piece + 24]] == [color_code] * 4:
                    return color_code
            if LEFT and UP:
                if [board[piece], board[piece - 8], board[piece - 16], board[piece - 24]] == [color_code] * 4:
                    return color_code
            if LEFT and DOWN:
                if [board[piece], board[piece + 6], board[piece + 12], board[piece + 18]] == [color_code] * 4:
                    return color_code

    for x in range(42): # check for draw state
        if board[x] == 0:
            # still playing
            return -1

    # draw game
    return 0

def get_dropped_loc(board, row):
    counter = 0
    for piece in range(row, row + 42, 7):
        if board[piece] == 0: # for every blank space
            counter += 1
    return row + (7 * (counter - 1))






class C4Env(Env):
    metadata = {'render.modes': ['human', 'developer']}
    def __init__ (self):
        self.action_space = Discrete(NUM_ROWS)
        self.observation_space =  Dict({"board": Box(low=0, high=2, shape=(42, ), dtype = np.uint8), "turn":  Box(low=1, high=2, shape=(1, ), dtype=np.uint8)})
        self.set_start_color('O')
        self.seed()
        self.reset()

    def set_start_color(self, color):
        self.start_color = color

    def step(self, action):
        assert self.action_space.contains(action)
        loc = get_dropped_loc(self.board, action)
        if self.done:
            return self.__get_obs(), 0, True, {None: None} # observation, reward, done, info 
        reward = NO_REWARD

        self.board[loc] = to_code(self.color) # place a piece
        status = check_game_status(self.board)

        # logboard = ""
        # for i, e in enumerate(self.board):
        #     if i % 7 == 0:
        #         logboard += "\n"
        #     logboard += str(e) + ","
        #print(f'Board_array: {logboard}\nColor: {self.color}\nStatus: {status}\nStatus Key: -1 = Ongoing, 0 = Draw, 1 = Yellow Win, 2 = Red Win')
        logging.debug(f'Board_array: {self.board}\nColor: {self.color}\nStatus: {status}\nStatus Key: -1 = Ongoing, 0 = Draw, 1 = Yellow Win, 2 = Red Win')
        
        if status >= 0: # game end
            self.done = True
            if status in [1, 2]:
                reward = YELLOW_REWARD if self.color == 'O' else RED_REWARD
        self.color = next_color(self.color)
        return self.__get_obs(), reward, self.done, {None: None}

    def render(self, mode = 'human', close = False):
        if close:
            return
        if mode == 'human':
            print(self.show_board())
            print()
        elif mode == 'developer':
            logboard = ""
            for i, e in enumerate(self.board):
                if i % 7 == 0:
                    logboard += "\n"
                logboard += str(e) + ","
            logging.info(logboard)
            logging.info('')

    def reset(self):

        self.board = [0] * NUM_LOCS
        self.avail_rows = [good for good in range(0,7)]
        self.color = self.start_color
        self.done = False
        return self.__get_obs()
        
    def available_actions(self):
        for row in self.avail_rows:
            if get_dropped_loc(self.board, row) < 0:
                self.avail_rows.remove(row)
        return self.avail_rows

    def show_episode(self, episode, mode = 'human'):
        if mode == 'human':
            print(f'Episode: {episode}')
        elif mode == 'developer':
            logging.info(f'Episode: {episode}')
    def show_board(self):
        godly_index = 0
        godly_string = ""
        for juice in self.board:
            if godly_index % 7 == 0:
                godly_string += "\n"
            disk = to_color(juice)
            if disk == ' ':
                godly_string += '   '
            else:
                godly_string += f'{USE_COLOR[disk]} O {END_C}'
            godly_index += 1
        return godly_string
    def show_turn(self, color, mode = 'human'):
        if mode == 'human':
            print(f'Current turn: {color}')
        elif mode == 'developer':
            logging.info(f'Current turn: {color}')
    def show_result(self, result, color, mode = 'human'):
        self._show_result(result, color, print if (mode == 'human') else logging.info)
    def _show_result(self, result, color, print_or_log):
        status = check_game_status(self.board)
        assert status >= 0
        if status == 0:
            print_or_log("--- Game Over! It's a draw! ---")
        else:
            message = f"Winner is '{to_color(status)}'!"
            print_or_log(f"--- Game Over ---\n" + message)
        print_or_log('')
    def __get_obs(self):
        x = np.array(self.board, dtype=np.uint8)
        y = np.array([to_code(self.color)], dtype=np.uint8)
        print(f'Board: {x} {type(x)}, Colorcode:{y} {type(y)}')
        return {"board": x, "turn": y}


