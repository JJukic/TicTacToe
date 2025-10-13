import random
import pickle
from tictactoe_env import TicTacToeEnv
from Agents.q_agent import QAgent

# === Q-Learning Parameter ===
episodes = 1000000              # Anzahl der Trainingsdurchläufe
epsilon = 1                     # Exploration (100% Zufällige Züge des Agents)
min_epsilon = 0.01              # kleine Wahrscheinlichkeit nach Training zu explorieren
decay_rate = 0.99995            # die Rate mit der epsilon nach jeder Episode reduziert wird

agent = QAgent(epsilon=epsilon)

# === Statistik ===
wins, losses, draws = 0, 0, 0

for episode in range(episodes):
    env = TicTacToeEnv()
    state = env.reset()
    done = False

    # abwechselnd spielt Agent als X oder O
    agent_is_X = (episode % 2 == 0)

    while not done:
        # Zustand aus Sicht des Agenten
        board_state = tuple(env.board)

        if agent_is_X:
            # Agent = X = 1
            actions = env.available_actions()
            action = agent.select_action(board_state, actions)
            next_state, reward, done = env.step(action)
        else:
            # Agent = O = -1 (spiegeln)
            state_flipped = tuple([-x for x in env.board])
            actions = env.available_actions()
            action = agent.select_action(state_flipped, actions)
            env.board[action] = -1  # Agent macht O-Zug
            next_state = tuple(env.board)
            reward = env.check_winner()
            if reward == -1:
                reward = 1  # Agent hat als O gewonnen
                done = True
            elif reward == 1:
                reward = -1  # Gegner hat als X gewonnen
                done = True
            elif 0 not in env.board:
                reward = 0
                done = True
            else:
                done = False

        # Belohnung anpassen
        if done:
            if reward == 1:
                reward = 2.0
                wins += 1
            elif reward == 0:
                reward = 0.5
                draws += 1
            elif reward == -1:
                reward = -10.0
                losses += 1
            agent.update(board_state, action, reward, tuple(env.board), done, [])
            break

        # Gegnerzug (zufällig, damit Agent robust lernt)
        opp_actions = env.available_actions()
        opp_action = random.choice(opp_actions)
        next_state, reward, done = env.step(opp_action)

        if done:
            if reward == 1:
                reward = -10.0
                losses += 1
            elif reward == 0:
                reward = 0.5
                draws += 1
            agent.update(board_state, action, reward, tuple(env.board), done, [])
            break

        agent.update(board_state, action, reward, tuple(env.board), done, env.available_actions())
        state = tuple(env.board)

    # Epsilon reduzieren
    epsilon = max(min_epsilon, epsilon * decay_rate)
    agent.epsilon = epsilon

    if episode % 10000 == 0:
        print(f"📘 Episode {episode} | ε = {epsilon:.4f} | Q-States: {len(agent.q_table)}")

# === Q-Tabelle speichern ===
with open("q_table.pkl", "wb") as f:
    pickle.dump(agent.q_table, f)

print("\nTraining abgeschlossen")
print(f"Siege: {wins} | Niederlagen: {losses} | Unentschieden: {draws}")
print(f"Q-Tabelle enthält {len(agent.q_table)} Zustände.")