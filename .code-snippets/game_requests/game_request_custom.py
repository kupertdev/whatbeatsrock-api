from whatbeatsrock.api.game import Game

async def main():
    game = Game(username="top")

    user_id = game.get_user_id()

    if not user_id:
        raise ValueError("Failed to get user ID.")
                
    # game.memory_storage.set("room_id", user_id)

    game.game_request("default custom word", "guess word", user_id)
