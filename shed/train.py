import os

import rlcard
import torch
from rlcard.agents import DQNAgent, RandomAgent, NFSPAgent
from rlcard.envs.registration import register
from rlcard.utils import (
    Logger,
    get_device,
    plot_curve,
    reorganize,
    set_seed,
    tournament,
)

from shed.agents.RandomAgent import RandomAgent
from shed.agents.ShedAgent import HumanAgent

SEED = 4299
ALGORITHM = "dqn"
NUM_EPISODES = 5_000  # 5000
EVALUATE_EVERY = 100  # 100
NUM_EVAL_GAMES = 200  # 2000
MIN_FULL_EVAL_EPISODES = 1_000
USE_TRAINED_ADVERSARY = False
LOG_DIR = "./logs"

register(
    env_id="shed",
    entry_point="shed.env.shed:ShedEnv",
)


def get_trained_agent(model_path, device=None):
    agent = torch.load(model_path, map_location=device)
    agent.set_device(device)
    return agent


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

    if ALGORITHM == "dqn":
        agent = DQNAgent(
            num_actions=env.num_actions,
            state_shape=env.state_shape[0],
            mlp_layers=[64, 64],
            device=device,
            replay_memory_init_size=256,
            batch_size=256,
            replay_memory_size=1_500_000,
            epsilon_decay_steps=1_000_000,  # roughly 2000 eps
            learning_rate=0.00005,
        )
    elif ALGORITHM == "nfsp":
        agent = NFSPAgent(
            num_actions=env.num_actions,
            state_shape=env.state_shape[0],
            hidden_layers_sizes=[64, 64],
            q_mlp_layers=[64, 64],
            device=device,
            batch_size=256,
            # save_path=args.log_dir,
            # save_every=args.save_every
        )
    else:
        raise ValueError("Provide an algorithm")

    agents = [agent]

    adversary = (
        get_trained_agent("./logs/trained-adversary.pth", device)
        if USE_TRAINED_ADVERSARY
        else RandomAgent(num_actions=env.num_actions)
    )
    for _ in range(1, env.num_players):
        agents.append(adversary)
    env.set_agents(agents)

    # Start training
    with Logger(LOG_DIR) as logger:
        for episode in range(NUM_EPISODES):
            logger.log(f"\nStarting episode {episode}")

            if ALGORITHM == "nfsp":
                agents[0].sample_episode_policy()

            # Generate data from the environment
            trajectories, payoffs = env.run(is_training=True)

            # Reorganise the data to be state, action, reward, next_state, done
            trajectories = reorganize(trajectories, payoffs)

            # Feed transitions into agent memory, and train the agent
            # Here, we assume that DQN always plays the first position
            # and the other players play randomly (if any)
            for ts in trajectories[0]:
                agent.feed(ts)

            # Evaluate the performance. Play with random agents.
            num_eval_games = 5 if episode < MIN_FULL_EVAL_EPISODES else NUM_EVAL_GAMES
            if episode % EVALUATE_EVERY == 0:
                logger.log_performance(
                    episode,
                    tournament(
                        env,
                        num_eval_games,
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
