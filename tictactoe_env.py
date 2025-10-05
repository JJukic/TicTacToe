class TicTacToeEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [0] * 9
        self.current_player = 1
        return self.get_state()

    def get_state(self):
        return tuple(self.board)

    def available_actions(self):
        return [i for i in range(9) if self.board[i] == 0]

    def make_move(self, action):
        if self.board[action] != 0:
            raise ValueError("Ungültiger Zug")
        self.board[action] = self.current_player
        self.current_player *= -1

    def check_winner(self):
        wins = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],    #horizontal
            [0, 3, 6], [1, 4, 7], [2, 5, 8],    #vertikal
            [0, 4, 8], [2, 4, 6]                #diagonal
        ]
        for combo in wins:
            values = [self.board[i] for i in combo]
            s = sum(values)
            if s == 3:
                return 1
            elif s == -3:
                return -1
        if 0 not in self.board:
            return 0
        return None

    def step(self, action):
        self.make_move(action)
        winner = self.check_winner()
        done = winner is not None
        reward = 0
        if done:
            reward = winner
        return self.get_state(), reward, done

    