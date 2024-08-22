from whatbeatsrock.api.game import Game
from whatbeatsrock.utils.id_generator.generators import IDGenerator

import asyncio

async def main():

    uuid_bytes = IDGenerator.generate_uuid_bytes()
    gid = IDGenerator.format_uuid_bytes_to_string(uuid_bytes)

    game = Game()
    await game.game_request("rock", "scissors", gid)

asyncio.run(main())