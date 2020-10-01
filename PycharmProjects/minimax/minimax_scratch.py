    def minimax_alphabeta(self, node, player, depth, alpha, beta):
        children = node.compute_and_get_children()
        if depth == 0 or len(children) == 0: #terminal state is when there are no more nodes to explore
            print("terminal state")
            state_value, node = self.evaluate_state_1(player, node)
            move = node.move
            print("node.move:", node.move)
        elif player == 0: #player is MAX
            print("if player == 0")
            state_value = float('-inf')
            player1 = 1
            for child in children:
                print("inside player 0 for loop")
                new_value, new_move = self.minimax_alphabeta(child, player1, depth-1, alpha, beta)
                print("update max value?")
                if new_value >= state_value:
                    print("yes we update")
                    state_value = new_value
                    move = child.move
                    print("child.move",child.move)
                alpha = max(alpha, state_value)
                if beta <= alpha:
                    break
        elif player == 1:
            print("if player === 1")
            state_value = float('inf')
            player0 = 0
            for child in children:
                new_value, new_move = self.minimax_alphabeta(child, player0, depth-1, alpha, beta)
                print("update min value?")
                if new_value < state_value:
                    print("yes we update min value")
                    state_value = new_value
                beta = min(beta, state_value)
                if beta <= alpha:
                    break
        else:
            print("oh shit")
            print("something wrong with the states here")
            ### restart the game?
        #print("move:", move)
        return state_value, move


    def evaluate_state_1(self, player, node): #get difference between player scores
        state = node.state
        scores = state.get_player_scores()
        player0_score = scores[0] #Max score
        player1_score = scores[1] #Min score
        return player0_score - player1_score, node
