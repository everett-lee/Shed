import argparse
import os
import time

import rlcard
import torch
from rlcard.agents import DQNAgent, RandomAgent, NFSPAgent
from rlcard.envs.registration import register
from rlcard.utils import (
    Logger,
    get_device,
    plot_curve,
    print_card,
    reorganize,
    set_seed,
    tournament,
)

from shed.agents.RandomAgent import RandomAgent
from shed.agents.ShedAgent import HumanAgent

SEED = 1337
NUM_GAMES = 100
USE_RANDOM = True

register(
    env_id="shed",
    entry_point="shed.env.shed:ShedEnv",
)

def get_trained_agent(model_path, device=None):
    agent = torch.load(model_path, map_location=device)
    agent.set_device(device)
    return agent


def evaluate():
    # Check whether gpu is available
    device = get_device()
    print(f"DEVICE: {device}")

    # Make the environment with seed
    env = rlcard.make(
        "shed",
        config={
            "seed": SEED,
        },
    )

    # Seed numpy, torch, random
    set_seed(SEED)

    if not USE_RANDOM:
        a_1 = get_trained_agent("good_models/model-28-12-10000-beats-me.pth", device=device)
        a_2 = get_trained_agent("good_models/model-30-12-30000.pth", device=device)
    else:
        a_1 = RandomAgent(num_actions=env.num_actions)
        a_2 = RandomAgent(num_actions=env.num_actions)

    agents = [a_1, a_2]
    agent_name = ["agent 1", "agent 2"]
    env.set_agents(agents)

    start = time.time()
    rewards = tournament(env, NUM_GAMES)
    for position, reward in enumerate(rewards):
        print(position, agent_name[position], reward)
    end = time.time()
    print(f"Time to run {NUM_GAMES} games: {end - start}")

# 500 TIMES RUN: (1, 161.98 secs), (2, 160.63 secs), (3, 160.17)
# 500 TIMES RUN: (1, 281.12)

if __name__ == "__main__":
    evaluate()
