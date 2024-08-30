from whatbeatsrock.api.game import Game

async def main():
    game = Game() # or Game(username="username")
    game.play_game()
