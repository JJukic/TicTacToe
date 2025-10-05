from tictactoe_env import TicTacToeEnv

env = TicTacToeEnv()
state = env.reset()
print("Startzustand:", state)

while True:
    print("Board:", env.board)
    actions = env.available_actions()
    print("Mögliche Züge:", actions)
    action = actions[0]
    state, reward, done = env.step(action)
    print("Zug gemacht, neuer Stand:", state)
    if done:
        print("Spiel vorbei ! Behlohnung:", reward)
        break
