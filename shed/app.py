import random
import time

import requests

import streamlit as st

from shed.utils.card_to_action import card_to_action, action_to_card
from shed.utils.card_to_symbol import card_to_symbol

PLAYER_ID = 0


def handle_click(card_action):
    if card_action != "Pickup":
        action = card_to_action[card_action]
    else:
        action = "Pickup"

    res = requests.post(f"http://localhost:8000/player/0/action/{action}")
    print("*"*100)
    print(res)
    time.sleep(0.5)

# Main Streamlit app
def main():
    # st.markdown(
    #     """
    # <style>
    # button {
    #     font-size: 30px  !important;
    #     height: 60px;
    #     width: 60px;
    # }
    # </style>
    # """,
    #     unsafe_allow_html=True,
    # )

    st.title("Shed")

    hand = requests.get("http://localhost:8000/player/0/hand").json()
    legal_actions = requests.get("http://localhost:8000/player/0/legal-actions").json()
    active_deck = requests.get("http://localhost:8000/player/0/active-deck").json()

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
    print("JJ"*100)
    print(legal_actions)
    print(legal_cards)
    legal_hand = [card for card in hand if card in legal_cards]
    print(hand)
    print(legal_hand)

    st.header("Player legal cards")
    if legal_hand:
        p1_hand_cols = st.columns(len(legal_hand))
        for i, col in enumerate(p1_hand_cols):
            with col:
                c = legal_hand[i]
                symbol = card_to_symbol[c]
                st.header(symbol)
                st.button(c, key=c, on_click=handle_click, args=[c])

    if "Pickup" in legal_actions:
        st.button("Pickup", key="Pickup", on_click=handle_click, args=["Pickup"])


    st.header("Active deck")
    st.write(f"hello {random.randint(0, 1000)}")

    if active_deck:
        print("*"*1000)
        print(active_deck)
        deck_cols = st.columns(len(active_deck))
        for i, col in enumerate(deck_cols):
            with col:
                card = active_deck[i]
                symbol = card_to_symbol[card]
                st.header(f"{card}{symbol}")


# Run the app
if __name__ == "__main__":
    main()
