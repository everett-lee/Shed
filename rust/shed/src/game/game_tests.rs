#[cfg(test)]
mod game_tests {
    use crate::{
        game::{action::Action, player::Player, game::Game},
        Card, Rank, Suit,
    };

    #[test]
    fn test_init_game() {
        let mut game = Game::new(2, None);
        game.init_game();
        assert!(!game.is_over());
        assert_eq!(game.get_player(0).hand().len(), 5);
        assert_eq!(game.get_player(1).hand().len(), 5);
        assert!(game.get_active_deck().is_empty())
    }


    #[test]
    fn test_step() {
        let mut game = Game::new(2, None);
        game.init_game();
        let legal_actions = game.get_legal_actions();
        // It is possible to have for of a kind, therefore minimum two actions
        assert!(game.get_legal_actions().len() >= 2);
        game.step(legal_actions.get(0).unwrap().clone());
        assert!(!game.get_active_deck().is_empty());
    }
}
