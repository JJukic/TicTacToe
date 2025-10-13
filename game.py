import tkinter as tk
import pickle
import random
from tictactoe_env import TicTacToeEnv
from Agents.q_agent import QAgent
from Agents.actor_critic_agent import ActorCriticAgent


# --- Globale Variablen ---
agent = None
current_agent_type = "qlearning"
agent_last_state = None
agent_last_action = None


# --- Agenten laden ---
def load_agent(agent_type="qlearning"):
    global agent, current_agent_type
    current_agent_type = agent_type

    if agent_type == "actorcritic":
        agent = ActorCriticAgent(n_states=3 ** 9, n_actions=9)
        try:
            with open("actor_critic.pkl", "rb") as f:
                data = pickle.load(f)
                agent.V = data["V"]
                agent.preferences = data["preferences"]
                print("✅ Actor-Critic geladen.")
        except FileNotFoundError:
            print("⚠️ Keine gespeicherte Actor-Critic-Datei gefunden – starte neu.")
    else:
        agent = QAgent(epsilon=0)
        try:
            with open("q_table.pkl", "rb") as f:
                agent.q_table = pickle.load(f)
                print("✅ Q-Learning-Agent geladen.")
        except FileNotFoundError:
            print("⚠️ Keine q_table.pkl gefunden – starte neu.")


# --- Environment + GUI Setup ---
env = TicTacToeEnv()
window = tk.Tk()
window.title("Tic Tac Toe – RL-Agent vs Mensch")
window.config(padx=20, pady=20)

# --- Agentenauswahl Dropdown ---
agent_var = tk.StringVar(value="qlearning")

def on_agent_change(*args):
    agent_type = agent_var.get()
    load_agent(agent_type)
    reset_game()

tk.Label(window, text="Agenten-Typ:", font=("Arial", 12)).grid(row=0, column=0, sticky="e")
agent_menu = tk.OptionMenu(window, agent_var, "qlearning", "actorcritic")
agent_menu.grid(row=0, column=1, sticky="w")
agent_var.trace("w", on_agent_change)

# --- Spielfeld und Labels ---
frame = tk.Frame(window)
frame.grid(row=1, column=0, columnspan=3)

status = tk.Label(window, text="Du spielst O", font=("Arial", 16))
status.grid(row=2, column=0, columnspan=3, pady=10)

score = {"agent": 0, "player": 0, "draw": 0}
score_label = tk.Label(window, text="", font=("Arial", 12))
score_label.grid(row=3, column=0, columnspan=3)


def update_score_label():
    score_label.config(
        text=f"🏆 Agent: {score['agent']}   🧍 Du: {score['player']}   🤝 Unentschieden: {score['draw']}"
    )


# --- Spiellogik ---
def on_click(pos):
    global agent_last_state, agent_last_action

    if env.board[pos] != 0:
        return

    # Spielerzug
    player_state = tuple(env.get_state())
    env.board[pos] = -1
    buttons[pos]["text"] = "O"
    buttons[pos]["state"] = "disabled"
    buttons[pos]["bg"] = "#e6f7ff"

    # Gewinner prüfen
    winner = env.check_winner()
    if winner is not None:
        reward = -10.0
        if agent_last_state is not None and agent_last_action is not None:
            agent.update(agent_last_state, agent_last_action, reward, None, True, [])
        show_winner(winner)
        return

    # Agentzug
    agent_state = tuple([-x for x in env.get_state()])
    action = agent.select_action(agent_state, env.available_actions())
    env.board[action] = 1
    buttons[action]["text"] = "X"
    buttons[action]["state"] = "disabled"
    buttons[action]["bg"] = "#ffe6e6"

    agent_last_state = agent_state
    agent_last_action = action

    winner = env.check_winner()
    if winner is not None:
        reward = 10.0 if winner == 1 else 0.5
        if agent_last_state is not None and agent_last_action is not None:
            agent.update(agent_last_state, agent_last_action, reward, None, True, [])
        show_winner(winner)
    else:
        agent.update(agent_last_state, agent_last_action, 0, tuple([-x for x in env.get_state()]), False, env.available_actions())


def show_winner(winner):
    if winner == 1:
        status.config(text="🤖 Agent (X) gewinnt!")
        score["agent"] += 1
    elif winner == -1:
        status.config(text="🎉 Du (O) gewinnst!")
        score["player"] += 1
    else:
        status.config(text="🤝 Unentschieden!")
        score["draw"] += 1

    update_score_label()
    for btn in buttons:
        btn["state"] = "disabled"


def reset_game():
    global env, agent_last_state, agent_last_action

    # Agent speichern
    if current_agent_type == "actorcritic":
        data = {"V": agent.V, "preferences": agent.preferences}
        with open("actor_critic.pkl", "wb") as f:
            pickle.dump(data, f)
    else:
        with open("q_table.pkl", "wb") as f:
            pickle.dump(agent.q_table, f)

    env = TicTacToeEnv()
    agent_last_state = None
    agent_last_action = None

    for btn in buttons:
        btn["text"] = ""
        btn["state"] = "normal"
        btn["bg"] = "white"

    # Epsilon-Decay nur für Q-Agent
    if hasattr(agent, "epsilon"):
        agent.epsilon = max(agent.epsilon * 0.995, 0.1)

    # Zufällig Startspieler
    if random.choice([True, False]):
        status.config(text=f"Agent ({current_agent_type}) beginnt (X)")
        state = tuple([-x for x in env.get_state()])
        action = agent.select_action(state, env.available_actions())
        env.board[action] = 1
        buttons[action]["text"] = "X"
        buttons[action]["state"] = "disabled"
        buttons[action]["bg"] = "#ffe6e6"
        agent_last_state = state
        agent_last_action = action
    else:
        status.config(text=f"Du beginnst (O) gegen {current_agent_type.upper()}")

    update_score_label()


# --- Spielfeld Buttons ---
buttons = []
for i in range(9):
    btn = tk.Button(frame, text="", width=6, height=3,
                    font=("Arial", 20),
                    bg="white",
                    command=lambda pos=i: on_click(pos))
    btn.grid(row=i // 3, column=i % 3)
    buttons.append(btn)

tk.Button(window, text="🔁 Neu starten", command=reset_game).grid(row=4, column=0, columnspan=3, pady=10)

# --- Start ---
load_agent("qlearning")
reset_game()
window.mainloop()