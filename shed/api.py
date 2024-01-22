import asyncio

import rlcard
from fastapi import FastAPI
from rlcard.envs.registration import register
from rlcard.utils import get_device

from shed.agents.AppShedAgent import AppAgent
from shed.agents.RandomAgent import RandomAgent
from shed.env.shed import ShedEnv
from shed.game.utils import ShedAction

app = FastAPI()
ENV = None

async def start_env():
    register(
        env_id="shed",
        entry_point="shed.env.shed:ShedEnv",
    )

    env: ShedEnv = rlcard.make(
        "shed",
        config={
            "debug_mode": True,
        },
    )
    global ENV
    ENV = env

    device = get_device()

    USE_TRAINED_AGENT = False
    # Human player always 0
    PLAYER_ID = 0

    app_agent = AppAgent(num_actions=env.num_actions)
    random_agent = RandomAgent(num_actions=env.num_actions)

    if USE_TRAINED_AGENT:
        pass
    else:
        env.set_agents([app_agent, random_agent])

    trajectories, payoffs = await env.run_async(is_training=False)

@app.get("/")
async def root():
    return "It's alive"

@app.post("/player/{id}/action/{action}")
async def send_action(id: int, action: ShedAction):
    ENV.set_next_action(id, action)

@app.get("/player/{id}/hand")
async def get_hand(id: int):
    return ENV.get_state(id)["hand"]

@app.get("/player/{id}/legal-actions")
async def get_hand(id: int):
    return ENV.get_state(id)["legal_actions"]

@app.get("/player/{id}/active-deck")
async def get_hand(id: int):
    return [c.get_index() for c in ENV.get_state(id)["active_deck"]]

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_env())

