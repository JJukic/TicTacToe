import random
import pickle
from tictactoe_env import TicTacToeEnv
from q_agent import QAgent

env = TicTacToeEnv()
agent = QAgent()

episodes = 10000
wins = 0
losses = 0
draws = 0

for episode in range(episodes):
    state = env.reset()
    done = False

    while not done:
        actions = env.available_actions()
        action = agent.select_action(state, actions)
        next_state, reward, done = env.step(action)

        if done:
            agent.update(state, action, reward, next_state, done, [])
            if reward == 1:
                wins += 1
            elif reward == -1:
                losses += 1
            else:
                draws += 1
            break

        opp_actions = env.available_actions()
        opp_action = random.choice(opp_actions)
        next_state, reward, done = env.step(opp_action)

        if done:
            agent.update(state, action, reward, next_state, done, [])
            if reward == 1:
                wins += 1
            elif reward == -1:
                losses += 1
            else:
                draws += 1
            break

        next_actions = env.available_actions()
        agent.update(state, action, reward, next_state, done, next_actions)
        state = next_state

    if episode % 1000 == 0:
        print(f"Episode {episode}")

# Speichern
with open("q_table.pkl", "wb") as f:
    pickle.dump(agent.q_table, f)

print("Q-Tabelle wurde gespeichert.")
print(f"Ergebnisse: Gewinne: {wins}, Verluste: {losses}, Unentschieden: {draws}")

