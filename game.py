import tkinter as tk
import pickle

from tictactoe_env import TicTacToeEnv
from q_agent import QAgent

# Spielfeld und Agent initialisieren
env = TicTacToeEnv()
agent = QAgent(epsilon=0)  # Kein Zufall – nur das Beste

# Q-Tabelle laden
try:
    with open("q_table.pkl", "rb") as f:
        agent.q_table = pickle.load(f)
    print("Q-Tabelle erfolgreich geladen.")
except FileNotFoundError:
    print("Fehler: q_table.pkl nicht gefunden. Bitte trainiere den Agenten zuerst.")
    exit()

# Fenster erstellen
window = tk.Tk()
window.title("Tic Tac Toe – Du vs RL-Agent")

buttons = []

# Spieler klickt auf ein Feld
def on_click(pos):
    if env.board[pos] != 0:
        return

    env.board[pos] = -1  # Mensch = O
    buttons[pos]["text"] = "O"
    buttons[pos]["state"] = "disabled"

    winner = env.check_winner()
    if winner is not None:
        show_winner(winner)
        return

    # Agent spielt (X)
    state = env.get_state()
    action = agent.select_action(state, env.available_actions())
    env.board[action] = 1
    buttons[action]["text"] = "X"
    buttons[action]["state"] = "disabled"

    winner = env.check_winner()
    if winner is not None:
        show_winner(winner)

# Gewinner anzeigen
def show_winner(winner):
    if winner == 1:
        result = "Agent (X) gewinnt!"
    elif winner == -1:
        result = "Du (O) gewinnst!"
    else:
        result = "Unentschieden!"
    label.config(text=result)
    for btn in buttons:
        btn["state"] = "disabled"

# Spiel Reset
def reset_game():
    global env
    env = TicTacToeEnv()
    for btn in buttons:
        btn["text"] = ""
        btn["state"] = "normal"
    label.config(text="Du spielst O")

# GUI-Elemente aufbauen
frame = tk.Frame(window)
frame.pack()

for i in range(9):
    btn = tk.Button(frame, text="", width=6, height=4,
                    font=("Arial", 20),
                    command=lambda pos=i: on_click(pos))
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

label = tk.Label(window, text="Du spielst O", font=("Arial", 16))
label.pack(pady=10)

reset_btn = tk.Button(window, text="Neu starten", command=reset_game)
reset_btn.pack()

# Spiel starten
window.mainloop()