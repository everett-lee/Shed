from rlcard.utils.utils import print_card


class AppAgent(object):
    def __init__(self, num_actions):
        """Initilize the human agent

        Args:
            num_actions (int): the size of the ouput action space
        """
        self.use_raw = True
        self.num_actions = num_actions

    @staticmethod
    def step(state):
        _print_state(state["raw_obs"], state["action_record"])
        action_input = input(">> You choose action (integer): ")
        while not action_input.isdigit():
            action_input = input(">> You choose action (integer): ")

        action = int(action_input)
        print(f"LEGAL ACTIONS = {state['legal_actions']}")
        print(f"RAW LEGAL ACTIONS = {state['raw_legal_actions']}")
        while action < 0 or action >= len(state["legal_actions"]):
            print("Action illegal...")
            action = int(input(">> Re-choose action (integer): "))
        return state["raw_legal_actions"][action]

    def eval_step(self, state):
        """Predict the action given the curent state for evaluation. The same to step here.

        Args:
            state (numpy.array): an numpy array that represents the current state

        Returns:
            action (int): the action predicted (randomly chosen) by the random agent
        """
        return self.step(state), {}


def _print_state(state, action_record):
    """Print out the state

    Args:
        state (dict): A dictionary of the raw state
        action_record (list): A list of the historical actions
    """

    _action_list = []
    for i in range(1, len(action_record) + 1):
        if action_record[-i][0] == state["current_player"]:
            break
        _action_list.insert(0, action_record[-i])
    for pair in _action_list:
        print(">> Player", pair[0], "chooses", pair[1])

    print("\n=============== Active deck ===============")
    print_card(state["active_deck"])

    print("=============  Player", state["current_player"], "- Hand   =============")
    card_chunks = [state["hand"][i : i + 10] for i in range(0, len(state["hand"]), 10)]
    for cards in card_chunks:
        print_card(cards)

    print("\n=========== Actions You Can Choose ===========")
    print(
        ", ".join(
            [
                str(index) + ": " + str(action)
                for index, action in enumerate(state["legal_actions"])
            ]
        )
    )
    print("")
