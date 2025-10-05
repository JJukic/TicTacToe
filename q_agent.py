import random
from collections import defaultdict

# Q-Werte Initialisierung (standardmäßig 0 für alle 9 Positionen)
def default_q_values():
    return [0] * 9

class QAgent:
    def __init__(self, alpha=0.5, gamma=0.95, epsilon=0.2):
        self.q_table = defaultdict(default_q_values)
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def select_action(self, state, available_actions):
        if random.random() < self.epsilon:
            return random.choice(available_actions)

        q_values = self.q_table[state]
        action_qs = [(a, q_values[a]) for a in available_actions]

        max_q = max(q for _, q in action_qs)
        best_actions = [a for a, q in action_qs if q == max_q]

        return random.choice(best_actions)

        print(f"Zustand: {state}")
        print(f"Q-Werte: {[round(q_values[a], 2) for a in range(9)]}")

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