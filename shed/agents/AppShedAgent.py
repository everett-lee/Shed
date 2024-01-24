import asyncio
import time

from shed.game.utils import ShedAction

MAX_TIME_TO_PLAY_SECS = 300

class AppAgent(object):
    def __init__(self, num_actions):
        """Initilize the human agent

        Args:
            num_actions (int): the size of the ouput action space
        """
        self.use_raw = True
        self.num_actions = num_actions
        self.next_app_agent_action = []

    def set_next_action(self, action: ShedAction):
        self.next_app_agent_action = [action]

    async def eval_step(self, state):
        start_time = time.time()
        while not self.next_app_agent_action:
            elapsed = time.time() - start_time
            print(f"WAITING for {elapsed}")
            if elapsed > MAX_TIME_TO_PLAY_SECS:
                raise Exception("Game timeout")
            await asyncio.sleep(0.01)

        action = self.next_app_agent_action.pop(0)

        return action, {}
