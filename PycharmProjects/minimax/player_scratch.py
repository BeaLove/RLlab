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
        #model = self.initialize_model(initial_data=first_msg)

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0) ##first node is created

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(
                initial_tree_node=node) ##send that root node to search_best_next_move()

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

    def search_best_next_move(self, initial_tree_node):
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
        ## initialize alpha, beta deoth etc with starting values
        alpha = float('-inf')
        beta = float('inf')
        depth = 4
        player = 0
        ##send root node and these parameters to minimax
        root_children = initial_tree_node.compute_and_get_children()
        values_and_moves = {}
        i = 0
        #for every child of the root node we run minimax, save child's move and state value in dict,
        # then choose best move based on highest value
        for child in root_children:
            i += 1
            print("iter:", i)
            state_value = self.minimax_alphabeta(child, player, depth, alpha, beta)
            print("state value:", state_value)
            print("move:", child.move)
            values_and_moves[child.move] = state_value
        print("values and moves: ", values_and_moves)
        best_value = max(values_and_moves.values())
        print("best value", best_value)
        best_move = list(values_and_moves.keys())[list(values_and_moves.values()).index(best_value)]
        print("best move", best_move)
        #random_move = random.randrange(5)
        return ACTION_TO_STR[best_move]

    def minimax_alphabeta(self, node, player, depth, alpha, beta):
        start_time = time()
        children = node.compute_and_get_children()
        if len(children) == 0 or time() - start_time >= 6e-3: #terminal state is when there are no more nodes to explore
            state_value = self.evaluate_state_1(player, node.state)
        elif player == 0: #player is MAX
            best_value = float('-inf')
            player1 = 1
            for child in children:
                new_value = self.minimax_alphabeta(child, player1, depth-1, alpha, beta)
                if new_value > best_value:
                    best_value = new_value
                    best_move = child.move
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
        elif player == 1:
            best_min_value = float('inf')
            player0 = 0
            for child in children:
                new_value = self.minimax_alphabeta(child, player0, depth-1, alpha, beta)
                if new_value < best_min_value:
                    best_min_value = new_value
                beta = min(beta, best_min_value)
                if beta <= alpha:
                    break
        else:
            print("oh shit")
            print("something wrong with the states here")
            ### restart the game?
        #print("move:", move)
        return best_move

    def evaluate_state_1(self, player, state): #get difference between player scores
        scores = state.get_player_scores()
        player0_score = scores[0] #Max score
        player1_score = scores[1] #Min score
        return player0_score - player1_score
