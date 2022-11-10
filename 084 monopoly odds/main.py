# In the game, Monopoly, the standard board is set up in the following way:
# p084_monopoly_board.png
# A player starts on the GO square and adds the scores on two 6-sided dice to 
# determine the number of squares they advance in a clockwise direction. 
# Without any further rules we would expect to visit each square with equal 
# probability: 2.5%. However, landing on G2J (Go To Jail), CC (community chest), 
# and CH (chance) changes this distribution.
# In addition to G2J, and one card from each of CC and CH, that orders the player 
# to go directly to jail, if a player rolls three consecutive doubles, they do 
# not advance the result of their 3rd roll. Instead they proceed directly to jail.
# At the beginning of the game, the CC and CH cards are shuffled. 
# When a player lands on CC or CH they take a card from the top of the respective 
# pile and, after following the instructions, it is returned to the bottom of the pile. 
# There are sixteen cards in each pile, but for the purpose of this problem we are 
# only concerned with cards that order a movement; any instruction not concerned 
# with movement will be ignored and the player will remain on the CC/CH square.
# Community Chest (2/16 cards):
#   Advance to GO
#   Go to JAIL
# Chance (10/16 cards):
#   Advance to GO
#   Go to JAIL
#   Go to C1
#   Go to E3
#   Go to H2
#   Go to R1
#   Go to next R (railway company)
#   Go to next R
#   Go to next U (utility company)
#   Go back 3 squares.
# The heart of this problem concerns the likelihood of visiting a particular square. 
# That is, the probability of finishing at that square after a roll. For this reason 
# it should be clear that, with the exception of G2J for which the probability of 
# finishing on it is zero, the CH squares will have the lowest probabilities, as 
# 5/8 request a movement to another square, and it is the final square that the 
# player finishes at on each roll that we are interested in. We shall make no 
# distinction between "Just Visiting" and being sent to JAIL, and we shall also 
# ignore the rule about requiring a double to "get out of jail", assuming that they 
# pay to get out on their next turn.
# By starting at GO and numbering the squares sequentially from 00 to 39 we can 
# concatenate these two-digit numbers to produce strings that correspond with sets 
# of squares.
# Statistically it can be shown that the three most popular squares, in order, are 
# JAIL (6.24%) = Square 10, E3 (3.18%) = Square 24, and GO (3.09%) = Square 00. 
# So these three most popular squares can be listed with the six-digit modal string: 
# 102400.
# If, instead of using two 6-sided dice, two 4-sided dice are used, find the 
# six-digit modal string.
# Result: 101524

from typing import Callable, Generator, Set, List, Tuple, Dict
import time
import sys

sys.path.append(".")
from util import Heap
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

D = 4
BOARD_SIZE = 40
GO = 0
JAIL = 10
G2J = 30
CC = {2, 17, 33}
CH = {7, 22, 36}

def next_railroad(space: int) -> int:
    if space < 5 or space >= 35:
        return 5
    if space < 15:
        return 15
    if space < 25:
        return 25
    return 35

def next_utility(space: int) -> int:
    if space < 12 or space >= 28:
        return 12
    return 28

def get_empty_board() -> List[float]:
    return [0.0 for _ in range(BOARD_SIZE)]

def get_empty_board_graph() -> List[List[float]]:
    return [[0.0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def add_dice_moves(board: List[List[float]]):
    # From each space, what are the probabilities you will end up at each
    # space from a normal dice roll

    # If this is your third double roll, after a non-double, 
    # go to jail instead.
    three_doubles = pow(1 / D, 3)
    # But if your roll four rolls ago was a double, then the last 
    # one sent you to jail and you just got out. 
    not_double = (1 - 1 / D)
    # You could also be just out of jail due to a chance or 
    # community chest card in one of the last two turns, 
    # so we need some further correction.
    # There are six ch and cc spaces and each has 1/16 go to jail cards.
    # This assumes even probability for each space which obviously isn't 
    # exactly true (it's what we're trying to figure out!) but maybe it's
    # okay as a first order approximation going into the problem.
    no_card_gtj = pow(1 - (6/40 * 1/16), 2)
    # You could also be just out of jail from landing on the go to jail 
    # space in the last two turns.
    no_space_gtj = pow(1 - 1/40, 2)
    jail_correction = three_doubles * not_double * no_card_gtj * no_space_gtj
    move_chance = (1 - jail_correction) / (D * D) 
    for space in range(BOARD_SIZE):
        for roll1 in range(D):
            for roll2 in range(D):
                board[space][(space + roll1 + roll2 + 2) % BOARD_SIZE] += move_chance
        board[space][JAIL] += jail_correction
        
def add_go_to_jail(board: List[List[float]]):
    # Any probability assigned to the go to jail space should be relocated to jail
    for space in range(BOARD_SIZE):
        board[space][JAIL] += board[space][G2J]
        board[space][G2J] = 0.0

def add_cc(board: List[List[float]]):
    # Reallocate probability assigned to community chest spaces
    normal_move_chance = 14 / 16
    for space in range(BOARD_SIZE):
        for cc in CC:
            special_chance = board[space][cc] * (1 - normal_move_chance)
            board[space][cc] -= special_chance
            board[space][GO] += special_chance / 2
            board[space][JAIL] += special_chance / 2

def add_chance(board: List[List[float]]):
    # Reallocate the probability assigned to chance spaces
    normal_move_chance = 6 / 16
    for space in range(BOARD_SIZE):
        for ch in CH:
            special_chance = board[space][ch] * (1 - normal_move_chance)
            board[space][ch] -= special_chance
            board[space][GO] += special_chance / 10
            board[space][JAIL] += special_chance / 10
            board[space][11] += special_chance / 10  # C1
            board[space][24] += special_chance / 10  # E3
            board[space][39] += special_chance / 10  # H2
            board[space][5] += special_chance / 10  # R1
            board[space][next_railroad(ch)] += special_chance / 5
            board[space][next_utility(ch)] += special_chance / 10
            board[space][(space - 3 + BOARD_SIZE) % BOARD_SIZE] += special_chance / 10

def get_board_graph() -> List[List[float]]:
    # From each space, what is the probability you will end up 
    # at each other space after your next roll?
    board = get_empty_board_graph()
    add_dice_moves(board)
    add_go_to_jail(board)
    # Note chance needs to go before community chest 
    # because chance's back 3 can put you on cc
    add_chance(board)  
    add_cc(board)
    return board

def get_next_turn(board_state: List[float], graph: List[List[float]]) -> List[float]:
    next_state = get_empty_board()
    # For each space in the start state, we distribute that space's 
    # probability to all the other spaces according to the ratios 
    # we previously determined.
    for start in range(BOARD_SIZE):
        to_distribute = board_state[start]
        for dest in range(BOARD_SIZE):
            next_state[dest] += to_distribute * graph[start][dest]
    return next_state

def diff_states(state1: List[float], state2: List[float]) -> float:
    # Get a metric of how much the probability distribution has changed
    # between two states.
    diff = 0
    for space in range(BOARD_SIZE):
        diff += abs(state1[space] - state2[space])
    return diff

def find_steady_state() -> List[float]:
    graph = get_board_graph()
    # Start with probability equally distributed
    start = [1/BOARD_SIZE for _ in range(BOARD_SIZE)]
    # Use the graph to redistribute the probability 
    # until we reach steady state.
    end = get_next_turn(start, graph)
    while diff_states(start, end) > 0.01:
        start = end
        end = get_next_turn(start, graph)
    return end

def modal_string(board_state: List[float]):
    # Make pairs of space and space probability
    pairs = [(i, board_state[i]) for i in range(len(board_state))]
    # Add to a max heap, so highest probability will be on top.
    # note reversed order to get a max heap instead of min
    heap = Heap(lambda a, b: b[1] - a[1], pairs)  
    top_3 = [heap.pop_root()[0] for _ in range(3)]
    ret = ""
    for space in top_3:
        if space < 10:
            ret += "0"
        ret += str(space)
    return ret

if __name__ == '__main__':
    """ starts here """
    start = time.time()
    print(modal_string(find_steady_state())) # 101524
    print(time.time() - start) # 0.0070 sec
