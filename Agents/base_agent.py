from abc import ABC, abstractmethod

class BaseAgent(ABC):
    @abstractmethod
    def select_action(self, state, legal_actions=None):
        ...

    @abstractmethod
    def update(self, state, action, reward, next_state, done, legal_actions_next=None):
        ...

    def on_episode_end(self):
        pass

    def save(self, path):
        pass

    def load(self, path):
        pass