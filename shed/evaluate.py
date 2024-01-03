import argparse
import os

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
NUM_GAMES = 50

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

    a_1 = get_trained_agent("good_models/model-28-12-10000-beats-me.pth", device=device)
    a_2 = get_trained_agent("good_models/model-30-12-30000.pth", device=device)
    agents = [a_1, a_2]
    agent_name = ["small older", "big daddy"]
    env.set_agents(agents)

    rewards = tournament(env, NUM_GAMES)
    for position, reward in enumerate(rewards):
        print(position, agent_name[position], reward)


if __name__ == "__main__":
    evaluate()
