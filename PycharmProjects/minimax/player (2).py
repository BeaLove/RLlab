#!/usr/bin/env python3
import random

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR
from time import time

class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate game tree object
        first_msg = self.receiver()
        # Initialize your minimax model
        model = self.initialize_model(initial_data=first_msg)

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(
                model=model, initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def initialize_model(self, initial_data):
        """
        Initialize your minimax model 
        :param initial_data: Game data for initializing minimax model
        :type initial_data: dict
        :return: Minimax model
        :rtype: object

        Sample initial data:
        { 'fish0': {'score': 11, 'type': 3}, 
          'fish1': {'score': 2, 'type': 1}, 
          ...
          'fish5': {'score': -10, 'type': 4},
          'game_over': False }

        Please note that the number of fishes and their types is not fixed between test cases.
        """
        # EDIT THIS METHOD TO RETURN A MINIMAX MODEL ###
        return None

    def search_best_next_move(self, model, initial_tree_node):
        """
        Use your minimax model to find best possible next move for player 0 (green boat)
        :param model: Minimax model
        :type model: object
        :param initial_tree_node: Initial game tree node 
        :type initial_tree_node: game_tree.Node 
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """

        # EDIT THIS METHOD TO RETURN BEST NEXT POSSIBLE MODE FROM MINIMAX MODEL ###
        
        # NOTE: Don't forget to initialize the children of the current node 
        #       with its compute_and_get_children() method!

        alpha = float('-inf')
        beta = float('inf')
        depth = 4
        player = 0
        ##send root node and these parameters to minimax
        move = self.minimax_alphabeta(initial_tree_node, player, depth, alpha, beta)
        #random_move = random.randrange(5)
        return ACTION_TO_STR[move]

    def minimax_alphabeta(self, node, player, depth, alpha, beta):
        """takes player (0 or 1 = MAX or MIN), state, current depth on search tree
        and alpha = best value achievable by MAX, beta = best achievable by min"""
        start_time = time()
        children = node.compute_and_get_children()
        if len(children) == 0 or time()-start_time >= 6e-3: #terminal state is when there are no more nodes to explore
            return self.evaluate_state(node)

        elif player == 0: #player is MAX
            state_value = float('-inf')
            player1 = 1
            for child in children:
                state_value = max(state_value, self.minimax_alphabeta(child, player1, depth-1, alpha, beta))
                alpha = max(alpha, state_value)
                print("alpha value at depth "+str(depth)+" is "+str(alpha))
                if beta <= alpha:
                    continue
        elif player == 1:
            state_value = float('inf')
            player0 = 0
            for child in children:
                state_value = min(state_value, self.minimax_alphabeta(child, player0, depth-1, alpha, beta))
                beta = min(beta, state_value)
                print("beta value at depth " + str(depth) + " is " + str(beta))
                if beta <= alpha:
                    continue


    def evaluate_state(self, node): #get difference between player scores
        state = node.state
        scores = state.get_player_scores()
        player0_score = scores[0] #Max score
        player1_score = scores[1] #Min score
        print(player0_score - player1_score)
        return int(player0_score - player1_score)
