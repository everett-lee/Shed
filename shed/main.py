import rlcard
from rlcard.envs.registration import register
from rlcard.utils import get_device, print_card

from shed.agents.RandomAgent import RandomAgent
from shed.agents.ShedAgent import HumanAgent
from shed.utils.model_utils import load_model

register(
    env_id="shed",
    entry_point="shed.env.shed:ShedEnv",
)

env = rlcard.make(
    "shed",
    config={
        "debug_mode": True,
    },
)

device = get_device()

USE_TRAINED_AGENT = True

human_agent = HumanAgent(num_actions=env.num_actions)
random_agent = RandomAgent(num_actions=env.num_actions)

if USE_TRAINED_AGENT:
    trained_agent = load_model(
        model_path="./good_models/23-1-5000.pth", device=device
    )
    env.set_agents([human_agent, trained_agent])
else:
    env.set_agents([human_agent, random_agent])

while True:
    print(">> Start a new game")

    trajectories, payoffs = env.run(is_training=False)
    # If the human does not take the final action, we need to
    # print other players action
    final_state = trajectories[0][-1]
    action_record = final_state["action_record"]
    state = final_state["raw_obs"]
    _action_list = []
    for i in range(1, len(action_record) + 1):
        if action_record[-i][0] == state["current_player"]:
            break
        _action_list.insert(0, action_record[-i])
    for pair in _action_list:
        print(">> Player", pair[0], "chooses", pair[1])

    print("===============     Result     ===============")
    print(payoffs)
    print("")

    input("Press any key to continue...")
