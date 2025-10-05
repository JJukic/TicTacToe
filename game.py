import tkinter as tk
import pickle
import random
from tictactoe_env import TicTacToeEnv
from q_agent import QAgent

agent_last_state = None
agent_last_action = None

# Agent laden
agent = QAgent(epsilon=0)
with open("q_table.pkl", "rb") as f:
    agent.q_table = pickle.load(f)

# GUI Setup
env = TicTacToeEnv()
window = tk.Tk()
window.title("Tic Tac Toe – RL-Agent vs Mensch")
window.config(padx=20, pady=20)

buttons = []
score = {"agent": 0, "player": 0, "draw": 0}

# GUI-Komponenten
frame = tk.Frame(window)
frame.grid(row=0, column=0, columnspan=3)

status = tk.Label(window, text="Du spielst O", font=("Arial", 16))
status.grid(row=1, column=0, columnspan=3, pady=10)

score_label = tk.Label(window, text="", font=("Arial", 12))
score_label.grid(row=2, column=0, columnspan=3)

def update_score_label():
    score_label.config(
        text=f"🏆 Agent: {score['agent']}   🧍 Du: {score['player']}   🤝 Unentschieden: {score['draw']}"
    )
def on_click(pos):
    global agent_last_state, agent_last_action

    if env.board[pos] != 0:  # Prüfe, ob das Feld bereits besetzt ist
        return

    # Zustand vor dem Zug des Spielers speichern
    player_state = tuple(env.get_state())

    # Spieler (Mensch) macht seinen Zug
    env.board[pos] = -1
    buttons[pos]["text"] = "O"
    buttons[pos]["state"] = "disabled"
    buttons[pos]["bg"] = "#e6f7ff"

    # Prüfe, ob der Mensch gewonnen hat
    winner = env.check_winner()
    if winner is not None:
        reward = -10.0  # Bestrafung für den Agenten, da der Mensch gewonnen hat
        if agent_last_state is not None and agent_last_action is not None:
            agent.update(agent_last_state, agent_last_action, reward, None, True, [])
        show_winner(winner)
        return

    # Agent trifft seine Entscheidung
    agent_state = tuple([-x for x in env.get_state()])  # Zustand für den Agenten (invertiert)
    action = agent.select_action(agent_state, env.available_actions())
    env.board[action] = 1  # Agent macht seinen Zug
    buttons[action]["text"] = "X"
    buttons[action]["state"] = "disabled"
    buttons[action]["bg"] = "#ffe6e6"

    # Speichere diesen Zustand und die Aktion für die nächste Runde
    agent_last_state = agent_state
    agent_last_action = action

    # Prüfe, ob der Agent gewonnen hat
    winner = env.check_winner()
    if winner is not None:
        reward = 10.0 if winner == 1 else 0.5  # Gewinn oder Unentschieden
        if agent_last_state is not None and agent_last_action is not None:
            agent.update(agent_last_state, agent_last_action, reward, None, True, [])
        show_winner(winner)
    else:
        # Aktualisiere Q-Werte des letzten Zuges
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

    # Speichere die aktualisierte Q-Tabelle
    with open("q_table.pkl", "wb") as f:
        pickle.dump(agent.q_table, f)

    # Neustart der Umgebung
    env = TicTacToeEnv()
    agent_last_state = None
    agent_last_action = None

    # Setze das Spielfeld zurück
    for i, btn in enumerate(buttons):
        btn["text"] = ""
        btn["state"] = "normal"
        btn["bg"] = "white"

    # Zufällig bestimmen, wer anfängt
    if random.choice([True, False]):
        status.config(text="Agent beginnt (X)")
        state = tuple([-x for x in env.get_state()])
        action = agent.select_action(state, env.available_actions())
        env.board[action] = 1
        buttons[action]["text"] = "X"
        buttons[action]["state"] = "disabled"
        buttons[action]["bg"] = "#ffe6e6"
        agent_last_state = state
        agent_last_action = action
    else:
        status.config(text="Du beginnst (O)")

    update_score_label()

    # Epsilon schrittweise reduzieren, um Exploration zu minimieren
agent.epsilon = max(agent.epsilon * 0.995, 0.1)  # Mindestens epsilon = 0.1

# Spielfeld erzeugen
for i in range(9):
    btn = tk.Button(frame, text="", width=6, height=3,
                    font=("Arial", 20),
                    bg="white",
                    command=lambda pos=i: on_click(pos))
    btn.grid(row=i // 3, column=i % 3)
    buttons.append(btn)

tk.Button(window, text="🔁 Neu starten", command=reset_game).grid(row=3, column=0, columnspan=3, pady=10)

# Starten
reset_game()
window.mainloop()