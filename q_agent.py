import random
from collections import defaultdict

# Q-Werte Initialisierung (standardmäßig 0 für alle 9 Positionen)
def default_q_values():
    return [0] * 9

class QAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = defaultdict(default_q_values)
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def select_action(self, state, available_actions):
        if random.random() < self.epsilon:
            return random.choice(available_actions)

        # Beste Aktion aus Q-Werten wählen (max Q)
        q_values = self.q_table[state]
        max_q = float('-inf')
        best_action = None

        for action in available_actions:
            if q_values[action] > max_q:
                max_q = q_values[action]
                best_action = action

        # Falls alle gleich: wähle zufällig aus den besten
        if best_action is None:
            return random.choice(available_actions)

        return best_action

    def update(self, state, action, reward, next_state, done, next_actions):
        q_values = self.q_table[state]
        current_q = q_values[action]

        if done:
            target = reward
        else:
            next_q_values = self.q_table[next_state]
            max_future_q = max([next_q_values[a] for a in next_actions]) if next_actions else 0
            target = reward + self.gamma * max_future_q

        # Q-Learning Update-Regel
        q_values[action] += self.alpha * (target - current_q)