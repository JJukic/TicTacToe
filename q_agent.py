import random
from collections import defaultdict

class QAgent:
    def __init__(self, epsilon=0.1, alpha=0.5, gamma=0.9):
        self.q_table = defaultdict(lambda: [0] * 9)
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

    def select_action(self, state, available_actions):
        if random.random() < self.epsilon:
            return random.choice(available_actions)
        q_values = self.q_table[state]
        best_action = max(available_actions, key=lambda a: q_values[a])
        return best_action

    def update(self, state, action, reward, next_state,done, available_actions):
        current_q = self.q_table[state][action]
        if done:
            target = reward
        else:
            next_q = max([self.q_table[next_state][a] for a in available_actions])
            target = reward + self.gamma * next_q

            self.q_table[state][action] += self.alpha * (target - current_q)

