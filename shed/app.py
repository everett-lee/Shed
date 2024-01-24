import random
import time
import uuid

import requests

import streamlit as st

from shed.utils.card_to_action import card_to_action, action_to_card
from shed.utils.card_to_symbol import card_to_symbol

st.set_page_config(layout="wide")
PLAYER_ID = 0

def handle_click(game_id: str, card_action: str):
    if card_action != "Pickup":
        action = card_to_action[card_action]
    else:
        action = "Pickup"

    res = requests.post(f"http://localhost:8000/game/{game_id}/player/0/action/{action}")
    print("*"*100)
    print(res)
    time.sleep(0.5)

def convert_active_deck(active_deck):
    return [f"{c['suit']}{c['rank']}" for c in active_deck]

# Main Streamlit app
def main():
    st.title("Shed")

    if "game_id" not in st.session_state:
        game_id = uuid.uuid4()
        st.session_state["game_id"] = game_id
        requests.post(f"http://localhost:8000/game/{game_id}")
    game_id = st.session_state["game_id"]

    winner = requests.get(f"http://localhost:8000/game/{game_id}/winner").json()
    if winner == 0:
        st.header("YOU WIN :)")
    elif winner >= 1:
        st.header("YOU LOST :(")
    else:
        state = requests.get(f"http://localhost:8000/game/{game_id}/player/0/state").json()
        opp_hand_size = requests.get(f"http://localhost:8000/game/{game_id}/player/1/hand-size").json()
        hand = state["hand"]
        legal_actions = state["legal_actions"]
        active_deck = convert_active_deck(state["active_deck"])
        unplayed_deck_size = state["unplayed_deck_size"]

        st.header("Player hand")
        if hand:
            p1_hand_cols = st.columns(len(hand))
            for i, col in enumerate(p1_hand_cols):
                with col:
                    c = hand[i]
                    symbol = card_to_symbol[c]
                    st.header(symbol)

        legal_cards = []
        for action in legal_actions:
            legal_cards.extend(action_to_card[action])
        legal_hand = [card for card in hand if card in legal_cards]

        st.header("Player legal cards")
        if legal_hand:
            p1_hand_cols = st.columns(len(legal_hand))
            for i, col in enumerate(p1_hand_cols):
                with col:
                    c = legal_hand[i]
                    symbol = card_to_symbol[c]
                    st.header(symbol)
                    st.button(c, key=c, on_click=handle_click, args=[game_id, c])

        if "Pickup" in legal_actions:
            st.button("Pickup", key="Pickup", on_click=handle_click, args=[game_id, "Pickup"])

        st.write(f"Unplayed deck size: {unplayed_deck_size}")
        st.write(f"Opponent hand size: {opp_hand_size}")
        st.header("Active deck")

        if active_deck:
            deck_cols = st.columns(len(active_deck))
            for i, col in enumerate(deck_cols):
                with col:
                    card = active_deck[i]
                    symbol = card_to_symbol[card]
                    st.header(f"{card}{symbol}")


# Run the app
if __name__ == "__main__":
    main()
