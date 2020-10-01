#!/usr/bin/env python3
import random

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR
from time import time
from random import random


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
        depth = 1
        player = 0
        ##send root node and these parameters to minimax
        start_time = time()
        move = self.minimax_alphabeta(initial_tree_node, player, depth, alpha, beta, start_time)
        #random_move = random.randrange(5)
        return ACTION_TO_STR[move[1]]

    def minimax_alphabeta(self, node, player, depth, alpha, beta, start_time):
        """takes player (0 or 1 = MAX or MIN), state, current depth on search tree
        and alpha = best value achievable by MAX, beta = best achievable by min"""
        children = node.compute_and_get_children()
        if len(children) == 0 or time() - start_time >= 0.05:
            # terminal state is when there are no more nodes to explore.HEURISTIC FUNCTION
            state_value, movement = self.evaluate_state3(node)
            #return state_value, movement

            # player0_score = scores[0]  # Max score
            # player1_score = scores[1]  # Min score
            # print("The scores are: " + str(player0_score - player1_score))
            # return float(player0_score - player1_score), mov
            # return float(-10 + random() * (10 - -10)), mov

        elif player == 0: #player is MAX
            state_value = float('-inf')
            player1 = 1
            for child in children:
                next_state_value, movement = self.minimax_alphabeta(child, player1, depth - 1, alpha, beta, start_time)
                if next_state_value > state_value:
                    state_value = next_state_value
                    movement = child.move
                #state_value = max(state_value, next_state_value)
                alpha = max(alpha, state_value)
                if alpha >= beta:
                    break
            # print("movement is:" + str(movement))
            #return state_value, movement

        elif player == 1:
            state_value = float('inf')
            player0 = 0
            for child in children:
                next_state_value, movement = self.minimax_alphabeta(child, player0, depth - 1, alpha, beta, start_time)
                if next_state_value < state_value:
                    state_value = next_state_value
                beta = min(beta, state_value)
                if beta <= alpha:
                    break
            # print("movement is:" + str(movement))
            #return state_value, movement
        return state_value, movement

    def evaluate_state2(self, node): #get difference between player scores
        scores = node.state.get_player_scores()
        player0_score = scores[0] #Max score
        player1_score = scores[1] #Min score
        return int(player0_score - player1_score)

    def evaluate_state(self, node):
        fish = node.state.get_fish_positions()
        player = node.state.get_hook_positions()
        distance1 = []
        vect1 = []
        distance2 = []
        vect2 = []
        print(fish)
        for f in fish.keys():
            print(f)
            distance1.append(
                self.compute_distance(fish[f], player[0])[0] + self.compute_distance(fish[f], player[0])[1])
            vect1.append(self.compute_distance(fish[f], player[0]))
            distance2.append(
                self.compute_distance(fish[f], player[1])[0] + self.compute_distance(fish[f], player[1])[1])
            vect2.append(self.compute_distance(fish[f], player[1]))
        closest_fish_index_ship1 = distance1.index(min(distance1))
        closest_fish_to_ship1 = min(distance1)
        closest_fish_to_ship2 = distance2[closest_fish_index_ship1]
        x = vect1[closest_fish_index_ship1][0]
        y = vect1[closest_fish_index_ship1][1]
        if x < y and x < 100:
            return closest_fish_to_ship1, 3
        if x < y and x > 100:
            return closest_fish_to_ship1, 4
        if y < x and y > player[0][1]:
            return closest_fish_to_ship1, 1
        if y < x and y > player[0][1]:
            return closest_fish_to_ship1, 2
        else:
            return closest_fish_to_ship1, 0

    def evaluate_state3(self, node):
        fish = node.state.get_fish_positions()
        players = node.state.get_hook_positions()
        sum_diff_distance = 0
        for fish in list(fish.values()):
            distance_player_max = abs(fish[0]-players[0][0]) + abs(fish[1]-players[0][1])
            distance_player_min = abs(fish[0] - players[1][0]) + abs(fish[1] - players[1][1])
            diff_distance = distance_player_max - distance_player_min
            sum_diff_distance += abs(diff_distance)
        return sum_diff_distance, node.move

    def compute_distance(self, position_fish, position_hook):
        dif_x = (position_hook[0]-position_fish[0])*(position_hook[0]-position_fish[0])
        dif_y = (position_hook[1]-position_fish[1])*(position_hook[1]-position_fish[1])
        print(dif_x, dif_y)
        return [dif_x, dif_y]
