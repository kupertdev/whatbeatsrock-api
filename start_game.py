from whatbeatsrock.api.game import Game

import logging
import asyncio

async def main():
    username = input("Enter username or pass: ").strip()
    game = Game(username=username, logging_level=logging.NOTSET)
    await game.play_game()

asyncio.run(main())