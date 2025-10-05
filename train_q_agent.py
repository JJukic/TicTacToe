import random
from tictactoe_env import TicTacToeEnv
from q_agent import QAgent

env = TicTacToeEnv()
agent = QAgent()

episodes = 1000

for episode in range(episodes):
    state = env.reset()
    done = False

    while not done:
        actions = env.available_actions()
        action = agent.select_action(state, actions)
        next_state, reward, done = env.step(action)

        if done:
            agent.update(state, action, reward, next_state, done, [])
            break

        opp_actions = env.available_actions()
        opp_action = random.choice(opp_actions)
        next_state, reward, done = env.step(opp_action)

        if done:
            agent.update(state, action, reward, next_state, done, [])
            break

        next_actions = env.available_actions()
        agent.update(state, action, reward, next_state, done, next_actions)
        state = next_state

