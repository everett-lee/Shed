import asyncio

from shed.game.utils import ShedAction


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
        while not self.next_app_agent_action:
            print("WAITING")
            await asyncio.sleep(0.5)

        action = self.next_app_agent_action.pop(0)

        print(f"FOUND ACTION {action}")

        return action, {}
