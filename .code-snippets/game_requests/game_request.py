from whatbeatsrock.api.game import Game
from whatbeatsrock.utils.id_generator.generators import IDGenerator

def main():

    gid = IDGenerator.generate_uuid_v4()

    game = Game()
    game.game_request("rock", "scissors", gid)
