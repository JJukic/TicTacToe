import numpy as np
from Agents.base_agent import BaseAgent

def softmax(x):
    x = x - np.max(x)
    e = np.exp(x)
    return e / np.sum(e)

class ActorCriticAgent(BaseAgent):
    def __init__(self, n_states, n_actions,
                 alpha_actor=0.05, alpha_critic=0.1, gamma=0.99):
        self.n_states = n_states
        self.n_actions = n_actions
        self.alpha_actor = alpha_actor
        self.alpha_critic = alpha_critic
        self.gamma = gamma

        self.V = np.zeros(n_states, dtype=np.float32)
        self.preferences = np.zeros((n_states, n_actions), dtype=np.float32)

    def _policy(self, s, legal_actions):
        prefs = self.preferences[s].copy()
        # nur legale Aktionen berücksichtigen
        mask = np.full_like(prefs, -1e9)
        for a in legal_actions:
            mask[a] = 0
        prefs += mask
        p = softmax(prefs)
        # Falls numerisch instabil → gleichverteilte Auswahl
        if np.any(np.isnan(p)) or np.sum(p) == 0:
            p = np.ones_like(p) / len(p)
        return p

    def select_action(self, state, legal_actions):
        # kleine Zufallskomponente (Exploration)
        epsilon = 0.1
        if np.random.rand() < epsilon:
            return np.random.choice(legal_actions)

        s = state if isinstance(state, int) else hash(state) % self.n_states
        probs = self._policy(s, legal_actions)
        return int(np.random.choice(np.arange(len(probs)), p=probs))

    def update(self, state, action, reward, next_state, done, legal_actions_next):
        s = state if isinstance(state, int) else hash(state) % self.n_states
        ns = s if next_state is None else (
            next_state if isinstance(next_state, int) else hash(next_state) % self.n_states
        )

        td_target = reward + (0 if done else self.gamma * self.V[ns])
        td_error = td_target - self.V[s]

        # Kritiker-Update
        self.V[s] += self.alpha_critic * td_error

        # Actor-Update
        probs = self._policy(s, list(range(self.n_actions)))
        grad = -probs
        grad[action] += 1.0
        self.preferences[s] += self.alpha_actor * td_error * grad