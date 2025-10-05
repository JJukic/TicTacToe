import tkinter as tk
import pickle
import random
from tictactoe_env import TicTacToeEnv
from q_agent import QAgent

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
    if env.board[pos] != 0:
        return

    env.board[pos] = -1
    buttons[pos]["text"] = "O"
    buttons[pos]["state"] = "disabled"
    buttons[pos]["bg"] = "#e6f7ff"

    winner = env.check_winner()
    if winner is not None:
        show_winner(winner)
        return

    # Agent spielt
    state = tuple([-x for x in env.get_state()])
    action = agent.select_action(state, env.available_actions())
    env.board[action] = 1
    buttons[action]["text"] = "X"
    buttons[action]["state"] = "disabled"
    buttons[action]["bg"] = "#ffe6e6"

    winner = env.check_winner()
    if winner is not None:
        show_winner(winner)

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
    global env
    env = TicTacToeEnv()
    for i, btn in enumerate(buttons):
        btn["text"] = ""
        btn["state"] = "normal"
        btn["bg"] = "white"

    # Zufällig starten lassen
    if random.choice([True, False]):
        status.config(text="Agent beginnt (X)")
        state = tuple([-x for x in env.get_state()])
        action = agent.select_action(state, env.available_actions())
        env.board[action] = 1
        buttons[action]["text"] = "X"
        buttons[action]["state"] = "disabled"
        buttons[action]["bg"] = "#ffe6e6"
    else:
        status.config(text="Du beginnst (O)")

    update_score_label()

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