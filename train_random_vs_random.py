import random
from tictactoe_env import TicTacToeEnv

env = TicTacToeEnv()
episodes = 5

for episode in range(episodes):
    state = env.reset()
    done = False

    print(f"\n Spiel {episode + 1} gestartet")

    while not done:
        actions = env.available_actions()
        action = random.choice(actions)
        state, reward, done = env.step(action)
        print(f"Agent spielt: {action}, Zustand: {state}")

        if done:
            print(f"Spielende! Reward: {reward}")
            break

        actions = env.available_actions()
        action = random.choice(actions)
        state, reward, done = env.step(action)
        print(f"Gegner spielt: {action}, Zustand: {state}")

        if done:
            print(f"Spielende! Reward: {reward}")
            break

