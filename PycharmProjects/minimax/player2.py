import random

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR


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
        depth = 3
        player = 0
        ##send root node and these parameters to minimax
        best_value, best_move = self.minimax(initial_tree_node, player, depth)
        print(best_move)
        return ACTION_TO_STR[best_move]

    def minimax(self, node, player, depth):
        children = node.compute_and_get_children()
        if len(children) == 0 or depth == 0:
            move = node.move
            print("move after state eval:", move)
            return self.evaluate_state(node.state), move

        else:
            if player == 0:
                best_value = float("-inf")
                player1 = 1
                for child in children:
                    state_value, max_move = self.minimax(child, player1, depth-1)
                    print("state value in max clause", state_value)
                    if state_value > best_value:
                        best_value = state_value
                        best_move = child.move
                print("best max move:", best_move)
                print("determined best max value", best_value)
                return best_value, best_move
            if player == 1:
                best_min_value = float("inf")
                player0 = 0
                for child in children:
                    min_value, min_move = self.minimax(child, player0, depth-1)
                    if min_value < best_min_value:
                        best_min_value = min_value
                        best_min_move = child.move
                return best_min_value, best_min_move

    def evaluate_state2(self, state): #get difference between player scores
        scores = state.get_player_scores()
        player0_score = scores[0] #Max score
        player1_score = scores[1] #Min score
        return player0_score - player1_score

    def compute_distance(self, state):
        fish = state.get_fish_positions()
        players = state.get_hook_positions()
        sum_diff_distance = 0
        for fish in list(fish.values()):
            distance_player_max = abs(fish[0]-players[0][0]) + abs(fish[1]-players[0][1])
            distance_player_min = abs(fish[0] - players[1][0]) + abs(fish[1] - players[1][1])
            diff_distance = distance_player_max - distance_player_min
            sum_diff_distance += abs(diff_distance)
        return sum_diff_distance
