import asyncio

import rlcard
from fastapi import FastAPI
from rlcard.envs.registration import register
from rlcard.utils import get_device

from shed.agents.AppShedAgent import AppAgent
from shed.agents.RandomAgent import RandomAgent
from shed.env.shed import ShedEnv
from shed.game.utils import ShedAction
from shed.utils.model_utils import load_model

app = FastAPI()

# TODO evict envs after time to avoid memory leaks
# TODO evict over max_games size
envs = {
}

winners = {}
register(
    env_id=f"shed",
    entry_point="shed.env.shed:ShedEnv",
)

# Human player always 0
PLAYER_ID = 0

device = get_device()
trained_agent = load_model(
    model_path="./good_models/24-1-7500-v-trained.pth", device=device
)
USE_TRAINED_AGENT = True

async def start_env(game_id: str):
    env: ShedEnv = rlcard.make(
        "shed",
        config={
            "debug_mode": True,
        },
    )
    envs[game_id] = env

    app_agent = AppAgent(num_actions=env.num_actions)
    random_agent = RandomAgent(num_actions=env.num_actions)

    if USE_TRAINED_AGENT:
        env.set_agents([app_agent, trained_agent])
    else:
        env.set_agents([app_agent, random_agent])

    try:
        trajectories, payoffs = await env.run_async(is_training=False)
        winners[game_id] = list(payoffs).index(1)
    except Exception as e:
        print(f"Game failed with {e}")
    finally:
        del envs[game_id]
        print(f"{len(envs)} games remaining")

@app.get("/")
async def root():
    return "It's alive"

@app.post("/game/{game_id}/player/{player_id}/action/{action}")
async def send_action(game_id: str, player_id: int, action: ShedAction):
    env = envs[game_id]
    env.set_next_action(player_id, action)

@app.get("/game/{game_id}/player/{player_id}/hand")
async def get_hand(game_id: str, player_id: int):
    env = envs[game_id]
    return env.get_game_state(player_id)["hand"]

@app.get("/game/{game_id}/player/{player_id}/legal-actions")
async def get_legal_action(game_id: str, player_id: int):
    env = envs[game_id]
    return env.get_game_state(player_id)["legal_actions"]

@app.get("/game/{game_id}/player/{player_id}/active-deck")
async def get_active_deck(game_id: str, player_id: int):
    env = envs[game_id]
    return [c.get_index() for c in env.get_game_state(player_id)["active_deck"]]

@app.get("/game/{game_id}/player/{player_id}/unplayed-deck-size")
async def get_unplayed_deck_size(game_id: str, player_id: int):
    env = envs[game_id]
    return env.get_game_state(player_id)["unplayed_deck_size"]

@app.get("/game/{game_id}/player/{player_id}/state")
async def get_unplayed_deck_size(game_id: str, player_id: int):
    env = envs[game_id]
    return env.get_game_state(player_id)

@app.get("/game/{game_id}/player/{player_id}/hand-size")
async def get_hand_size(game_id: str, player_id: int):
    env = envs[game_id]
    return len(env.get_game_state(player_id)["hand"])

@app.get("/game/{game_id}/winner")
async def get_unplayed_deck_size(game_id: str):
    if game_id in winners:
        return winners[game_id]
    return -1
@app.post("/game/{game_id}")
async def startup_event(game_id: str):
    asyncio.create_task(start_env(game_id))

