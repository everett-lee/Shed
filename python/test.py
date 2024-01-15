import rust_shed

a = rust_shed.Game(2, False)
print(a.get_num_players())
print(a.get_player_id())
a.init_game()
print(a.get_legal_actions())