from whatbeatsrock.api.game import Game
import asyncio

async def main():
    game = Game() # or Game(username="username")
    await game.play_game()

asyncio.run(main())