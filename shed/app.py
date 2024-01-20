import rlcard
from rlcard.envs.registration import register
from rlcard.utils import get_device

from shed.agents.RandomAgent import RandomAgent
from shed.agents.ShedAgent import HumanAgent

import streamlit as st
import random

from shed.utils.card_to_symbol import card_to_symbol


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

USE_TRAINED_AGENT = False

human_agent = HumanAgent(num_actions=env.num_actions)
random_agent = RandomAgent(num_actions=env.num_actions)

if USE_TRAINED_AGENT:
    pass
else:
    env.set_agents([human_agent, random_agent])

# Function to initialize the shared deck and players' hands
def initialize_game():
    player1_hand = ["SK", "H2"]
    player2_hand = ["C1", "D5"]
    return player1_hand, player2_hand

def handle_click(card):
    st.session_state["deck"] = st.session_state["deck"] + [card]

# Main Streamlit app
def main():
    st.title("Shed")
    
    if 'deck' not in st.session_state:
        st.session_state['deck'] = []

    # Initialize the game
    player1_hand, player2_hand = initialize_game()

    st.header("Player 1")
    if player1_hand:
        p1_hand_cols = st.columns(len(player1_hand))
        for i, col in enumerate(p1_hand_cols):
            with col:
                c = player1_hand[i]
                st.button(c, key=c, on_click=handle_click, args=[c])

    st.header("Shared deck")
    st.write(f"hello {random.randint(0, 1000)}")

    if st.session_state["deck"]:
        deck_cols = st.columns(len(st.session_state["deck"]))
        for i, col in enumerate(deck_cols):
            with col:
                card = st.session_state["deck"][i]
                symbol = card_to_symbol[card]
                st.header(f"{card}{symbol}")

# Run the app
if __name__ == "__main__":
    main()