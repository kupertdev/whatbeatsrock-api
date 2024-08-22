from whatbeatsrock.api.game import Game

import asyncio

async def main():
    game = Game(username="top")

    user_id = await game.get_user_id()

    if not user_id:
        raise ValueError("Failed to get user ID.")
                
    game.memory_storage.set("room_id", user_id)

    await game.get_custom_game_info()

    # await game.get_custom_game_info("1e9f7e25-7a02-4ff4-8662-f8b3e823be1b")

asyncio.run(main())