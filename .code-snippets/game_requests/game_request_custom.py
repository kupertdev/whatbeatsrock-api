from whatbeatsrock.api.game import Game

import asyncio

async def main():
    game = Game(username="top")

    user_id = await game.get_user_id()

    if not user_id:
        raise ValueError("Failed to get user ID.")
                
    # game.memory_storage.set("room_id", user_id)

    await game.game_request("default custom word", "guess word", user_id)

asyncio.run(main())