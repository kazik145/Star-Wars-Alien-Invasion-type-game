class GameStats:
    """Track statistics for Alien Invasion."""
    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.number_of_shots = []
        self.game_active = False
        # High score should never be reset.
        with open("All_time_hs.txt") as aths:
            all_time_hs = int(aths.read())
        self.high_score = all_time_hs

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1




