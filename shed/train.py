import argparse
import os

import rlcard
import torch
from rlcard.agents import DQNAgent, RandomAgent
from rlcard.envs.registration import register
from rlcard.utils import (Logger, get_device, plot_curve, print_card,
                          reorganize, set_seed, tournament)

from shed.agents.RandomAgent import RandomAgent
from shed.agents.ShedAgent import HumanAgent

SEED = 42
ALGORITHM = "dqn"
NUM_EPISODES = 50  # 5000
EVALUATE_EVERY = 10  # 100
NUM_EVAL_GAMES = 10  # 2000
LOG_DIR = "./logs"

register(
    env_id="shed",
    entry_point="shed.env.shed:ShedEnv",
)


def train():
    # Check whether gpu is available
    device = get_device()
    print(f"DEVICE: {device}")

    # Seed numpy, torch, random
    set_seed(SEED)

    # Make the environment with seed
    env = rlcard.make(
        "shed",
        config={
            "seed": SEED,
        },
    )

    agent = DQNAgent(
        num_actions=env.num_actions,
        state_shape=env.state_shape[0],
        mlp_layers=[64, 64],
        device=device,
    )
    agents = [agent]

    for _ in range(1, env.num_players):
        agents.append(RandomAgent(num_actions=env.num_actions))
    env.set_agents(agents)

    # Start training
    with Logger(LOG_DIR) as logger:
        for episode in range(NUM_EPISODES):
            # Generate data from the environment
            trajectories, payoffs = env.run(is_training=True)

            # Reorganaize the data to be state, action, reward, next_state, done
            trajectories = reorganize(trajectories, payoffs)

            # Feed transitions into agent memory, and train the agent
            # Here, we assume that DQN always plays the first position
            # and the other players play randomly (if any)
            for ts in trajectories[0]:
                agent.feed(ts)

            # Evaluate the performance. Play with random agents.
            if episode % EVALUATE_EVERY == 0:
                logger.log_performance(
                    episode,
                    tournament(
                        env,
                        NUM_EVAL_GAMES,
                    )[0],
                )

        # Get the paths
        csv_path, fig_path = logger.csv_path, logger.fig_path

    # Plot the learning curve
    plot_curve(csv_path, fig_path, ALGORITHM)

    # Save model
    save_path = os.path.join(LOG_DIR, "model.pth")
    torch.save(agent, save_path)
    print("Model saved in", save_path)


if __name__ == "__main__":
    train()
