# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script simulates 50,000 tic-tac-toe games between player 'X' and player 'O'.
Player 'X' always makes the first move, and both players choose an option randomly.
It outputs the win rate for both players, as well as the tie rate.
"""

__author__ = 'Moody Billah'
__date__ = '2021-02-20'
__course__ = 'STATS404'
__assignment__ = 'Extra Credit 1'

# Libraries
import random
random.seed(100)

def make_move(board, options, player, move_num):
    """This function conducts a single move for a player during a tic-tac-toe game.
    
    Args:
        board (dict): Current version of the tic-tac-toe board.
        options (list): Currently available move options on the tic-tac-toe board.
        player (str): Name of the player which is either 'X' or 'O'.
        move_num (int): Current number of moves by this player.
    
    Returns:
        board (dict): Updated version of the tic-tac-toe board after the move is made.
        options (list): Updated move options after the current move is removed.
        win (Bool): True if this player has won the game, False otherwise.
        move_num (int): Updated number of moves by this player by adding 1.
    
    """
    
    # Player makes a move on the tic-tac-toe board.
    move = random.sample(options, 1)[0]
    board[move] = player
    options.remove(move)
    move_num += 1
    
    # Check to see if the player won after each move, starting from the third move.
    if move_num >= 3:        
        win_conditions = [
                          {'top-L': player, 'top-M': player, 'top-R': player}, 
                          {'mid-L': player, 'mid-M': player, 'mid-R': player},
                          {'low-L': player, 'low-M': player, 'low-R': player},
                          {'top-L': player, 'mid-L': player, 'low-L': player}, 
                          {'top-M': player, 'mid-M': player, 'low-M': player},
                          {'top-R': player, 'mid-R': player, 'low-R': player},
                          {'top-L': player, 'mid-M': player, 'low-R': player},
                          {'top-R': player, 'mid-M': player, 'low-L': player},
                         ]
        
        win_list = [False] * len(win_conditions)   
        for i in range(len(win_list)):
            win_list[i] = win_conditions[i].items() <= board.items()      
        
        win = sum(win_list) > 0
    
    else:
        win = False
    
    return board, options, win, move_num

def play_game(scores):
    """This function conducts an entire tic-tac-toe game between 2 players.
    
    Implementation of is this function dependent on the make_move() function.
    
    Args:
        scores (dict): Initial scores of players with 0 wins and ties.
    
    Returns:
        scores (dict): Updated scores counting the number of wins for both players, as well as ties.
    
    """
    
    # Initialize input variables for the make_move() function.
    board = {
             'top-L': ' ', 'top-M': ' ', 'top-R': ' ',
             'mid-L': ' ', 'mid-M': ' ', 'mid-R': ' ',
             'low-L': ' ', 'low-M': ' ', 'low-R': ' '
            }
    options = list(board.keys())
    move_X = 0
    move_O = 0
    
    # Make moves alternately between each player until one of them win, or there is a tie.
    while len(options) > 0:       
        
        board, options, win_X, move_X = make_move(board, options, 'X', move_X)
        if win_X == True:
            scores['win_X'] +=1
            break
    
        if len(options) == 0:
            scores['win_O'] +=1
            break
    
        board, options, win_O, move_O = make_move(board, options, 'O', move_O)
        if win_O == True:
            scores['tie'] +=1
            break
    
    return scores

# Play 50,000 tic-tac-toe games and record the total scores.
scores = {'win_X': 0, 'win_O': 0, 'tie': 0}
for i in range(50000):
    play_game(scores)

# Calculate the win and tie rates based on the total scores.
rate_calc = lambda x: x / 50000
rate_list = list(map(rate_calc, scores.values()))
scores_rate = {'win_X': rate_list[0], 'win_O': rate_list[1], 'tie': rate_list[2]}

print(scores_rate)

# According to this simulation, player 'X' win rate, player 'O' win rate, and tie rate are about
# 59%, 12%, and 29% respectively. Although tic-tac-toe is meant to be a fair game when played randomly,
# there is a bias in this case because player 'X' always goes first. This gives them an extra turn,
# resulting in their win rate being significantly higher.
