import pickle
import random
import numpy as np
from tictactoe_env import TicTacToeEnv
from Agents.q_agent import QAgent
from Agents.actor_critic_agent import ActorCriticAgent


def main(agent_type="qlearning", episodes=50000):
    env = TicTacToeEnv()
    n_states = 3 ** 9
    n_actions = 9

    # === Agent initialisieren ===
    if agent_type.lower() == "actorcritic":
        agent = ActorCriticAgent(n_states, n_actions)
        print("🎭 Training Actor-Critic-Agent")
    else:
        agent = QAgent(epsilon=1.0)
        print("🧠 Training Q-Learning-Agent")

    # === Trainingsparameter ===
    epsilon = getattr(agent, "epsilon", 1.0)
    min_epsilon = 0.05
    decay_rate = 0.9999

    wins, losses, draws = 0, 0, 0

    # === Training ===
    for episode in range(1, episodes + 1):
        env.reset()
        done = False

        # Agent spielt abwechselnd als X (1) oder O (-1)
        agent_is_X = (episode % 2 == 0)

        while not done:
            # Zustand aus Sicht des Agenten
            board_state = tuple(env.board)

            # === Agent-Zug ===
            if agent_is_X:
                legal_actions = env.available_actions()
                action = agent.select_action(board_state, legal_actions)
                next_state, reward, done = env.step(action)
            else:
                # Agent spielt als O → invertiere Board
                state_flipped = tuple([-x for x in env.board])
                legal_actions = env.available_actions()
                action = agent.select_action(state_flipped, legal_actions)
                env.board[action] = -1
                next_state = tuple(env.board)
                winner = env.check_winner()

                if winner == -1:
                    reward = 1.0
                    done = True
                elif winner == 1:
                    reward = -1.0
                    done = True
                elif 0 not in env.board:
                    reward = 0.5
                    done = True
                else:
                    reward = -0.01
                    done = False

            # === Ende prüfen / Agent updaten ===
            if done:
                if reward > 0:
                    wins += 1
                elif reward < 0:
                    losses += 1
                else:
                    draws += 1
                agent.update(board_state, action, reward, tuple(env.board), done, [])
                break

            # === Gegnerzug (random) ===
            opp_actions = env.available_actions()
            if not opp_actions:
                break
            opp_action = random.choice(opp_actions)
            next_state, reward, done = env.step(opp_action)

            if done:
                winner = env.check_winner()
                if winner == 1:
                    reward = -1.0
                    losses += 1
                elif winner == -1:
                    reward = 1.0
                    wins += 1
                else:
                    reward = 0.5
                    draws += 1
                agent.update(board_state, action, reward, tuple(env.board), done, [])
                break

            # === Zwischenupdate ===
            agent.update(board_state, action, reward, tuple(env.board), done, env.available_actions())

        # === Exploration verringern (nur für Q-Learning) ===
        if hasattr(agent, "epsilon"):
            epsilon = max(min_epsilon, epsilon * decay_rate)
            agent.epsilon = epsilon

        # === Fortschritt ===
        if episode % max(1, episodes // 10) == 0:
            print(f"📘 Episode {episode}/{episodes} | ε={epsilon:.3f} | W:{wins} D:{draws} L:{losses}")

    # === Zusammenfassung ===
    print("\nTraining abgeschlossen.")
    print(f"🏆 Siege: {wins} | 😞 Niederlagen: {losses} | 🤝 Unentschieden: {draws}")

    # === Ergebnisse speichern ===
    if agent_type.lower() == "actorcritic":
        data = {"V": agent.V, "preferences": agent.preferences}
        with open("actor_critic.pkl", "wb") as f:
            pickle.dump(data, f)
        print("💾 Actor-Critic-Parameter gespeichert in actor_critic.pkl")
    else:
        with open("q_table.pkl", "wb") as f:
            pickle.dump(agent.q_table, f)
        print("💾 Q-Table gespeichert in q_table.pkl")


# === Script starten ===
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        main(sys.argv[1], int(sys.argv[2]))
    elif len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("qlearning")