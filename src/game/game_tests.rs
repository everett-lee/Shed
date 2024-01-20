#[cfg(test)]
mod game_tests {
    use crate::game::game::Game;


    #[test]
    fn test_position() {
        let mut game = Game::new(2, false);
        game.init_game();

        for _ in 0..40 {
            match game.get_legal_actions().get(0) {
                Some(action) => { game.step(action.clone()); }
                None => return
            }
        }

        let s1 = game.get_state(0);
        let s2 = game.get_state(1);
    

        if s1.hand.len() < s2.hand.len() {
            assert!(s1.position > s2.position)
        } else if s1.hand.len() > s2.hand.len() {
            assert!(s1.position < s2.position)
        }

    }

}