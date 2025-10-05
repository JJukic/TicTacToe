import tkinter as tk
from tictactoe_env import TicTacToeEnv
from q_agent import QAgent

env = TicTacToeEnv()
agent = QAgent(epsilon=0)

window = tk.Tk()
window.title("Tic Tac Toe – Du vs RL-Agent")

buttons = []

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

    # Agent spielt
    state = env.get_state()
    action = agent.select_action(state, env.available_actions())
    env.board[action] = 1
    buttons[action]["text"] = "X"
    buttons[action]["state"] = "disabled"

    winner = env.check_winner()
    if winner is not None:
        show_winner(winner)

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

def reset_game():
    global env
    env = TicTacToeEnv()
    for btn in buttons:
        btn["text"] = ""
        btn["state"] = "normal"
    label.config(text="Du spielst O")

# Spielfeld
frame = tk.Frame(window)
frame.pack()

for i in range(9):
    btn = tk.Button(frame, text="", width=6, height=3,
                    font=("Arial", 20),
                    command=lambda pos=i: on_click(pos))
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

label = tk.Label(window, text="Du spielst O", font=("Arial", 16))
label.pack(pady=10)

reset_btn = tk.Button(window, text="Neu starten", command=reset_game)
reset_btn.pack()

window.mainloop()