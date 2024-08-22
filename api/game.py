import asyncio
import logging

import httpx
from faker import Faker

from whatbeatsrock.utils import *


def add_memory_objects(storage_obj: MemoryStorage, keys: list, values: list):
    for key, value in zip(keys, values):
        storage_obj.set(key, value)


class Game:
    def __init__(
        self,
        username: str = None,
        wait_for_response_time: float = 10.0,
        connect_timeout: float = 5.0,
        logging_level: int = logging.DEBUG,
    ):
        self.api_endpoints: ApiEndpoints = ApiEndpoints()
        self.username: str = username
        self.memory_storage: MemoryStorage = MemoryStorage()

        self.headers: dict = {
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Origin": "https://www.whatbeatsrock.com",
            "Connection": "keep-alive",
            "User-Agent": Faker().user_agent(),
            "Accept": "*/*",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        }

        self.logger: logging.Logger = self.__create_logger(logging_level)

        self.wait_for_response_time: float = wait_for_response_time
        self.connect_timeout: float = connect_timeout

    def __create_logger(self, logging_level: int) -> logging.Logger:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging_level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging_level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

        return logger

    async def get_user_id(self) -> str:
        """
        Fetch the user ID for the given username.

        Returns:
            str: The user ID.

        Example:
            >>> game = Game(username="top")
            >>> game.get_user_id()
        """
        url = self.api_endpoints.user_info.format(username=self.username)

        user_data = await self.make_request("GET", url, None)

        return user_data["data"]["id"]

    async def get_custom_game_info(self, room_id: str = None):
        """
        Fetch custom game info from the API.

        Returns:
            dict: The API response containing game information.

        Example:
            >>> memory_storage.set("room_id", "123")
            >>> await game.get_custom_game_info()
        """
        user_id = self.memory_storage.get("room_id") if not room_id else room_id
        url = self.api_endpoints.game_info.format(user_id=user_id)

        room_info = await self.make_request("GET", url, None)
        return room_info

    async def game_request(self, previous_guess: str, guessed_word: str, room_id: str):
        """
        Send a game request to the API.

        Args:
            previous_guess (str): The previous guess.
            guessed_word (str): The guessed word.
            room_id (str): The room ID.

        Returns:
            dict: The API response.

        Example:
            >>> game_request("rock", "scissors", "123")
        """
        url = self.api_endpoints.api_vs

        data = {
            "prev": previous_guess,
            "guess": guessed_word,
            "gid" if not self.username else "oid": room_id,
        }

        response_data = await self.make_request("POST", url, data)

        return response_data.get("data", {})

    async def make_request(
        self, method: str = None, url: str = None, json_data: dict = None
    ) -> dict:
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(
                self.wait_for_response_time, connect=self.connect_timeout
            )
        ) as client:
            response = await client.request(
                method, url, headers=self.headers, json=json_data
            )
            self.logger.info(f"Status Code: {response.status_code}")
            self.logger.debug(f"{url} - {json_data}")
            if response.status_code != 200:
                self.logger.error(f"Received status code {response.status_code}")
            try:
                json_response = response.json()
                self.logger.debug(f"{url} - {json_response}")
                return json_response
            except ValueError:
                self.logger.error("JSON error. The request did not return json")

    async def play_game(self):
        """Main game loop."""
        if not self.username:

            uuid_bytes = IDGenerator.generate_uuid_bytes()
            room_id = IDGenerator.format_uuid_bytes_to_string(uuid_bytes)

            keys = [
                "previous_guess",
                "judgingCriteria",
                "judgingCriteriaLoss",
                "room_id",
            ]
            values = ["rock", "beats", "does not beat", room_id]

            add_memory_objects(self.memory_storage, keys, values)

        else:
            start_key = "attribute_data"
            user_id = await self.get_user_id()

            if not user_id:
                self.logger.error("Failed to get user ID.")
                raise ValueError("Failed to get user ID.")

            self.memory_storage.set("room_id", user_id)
            game_info = await self.get_custom_game_info()
            game_info = game_info["data"]

            keys = ["previous_guess", "judgingCriteria", "judgingCriteriaLoss"]
            values = [
                game_info[start_key]["startWord"],
                game_info[start_key]["judgingCriteria"],
                game_info[start_key]["judgingCriteriaLoss"],
            ]

            add_memory_objects(self.memory_storage, keys, values)

        while True:
            previous_guess = self.memory_storage.get("previous_guess")
            start_phrase = self.memory_storage.get("judgingCriteria")

            print(f"What {start_phrase} {previous_guess}?")

            guessed_word = input("Enter your guess: ").strip()
            room_id = self.memory_storage.get("room_id")
            result: dict = await self.game_request(
                previous_guess, guessed_word, room_id
            )

            if result.get("guess_wins", False) is False:
                loss_phrase = self.memory_storage.get("judgingCriteriaLoss")
                prev_word = self.memory_storage.get("previous_guess")
                print(
                    f"Sorry dear, you lose! {prev_word} {loss_phrase} {guessed_word}!\n\n{result.get('reason', '')}"
                )
                exit(1)

            reason = result.get("reason", "")
            print(
                f"Good Job! {guessed_word} {start_phrase} {previous_guess}!\n\n{reason}"
            )

            self.memory_storage.set("previous_guess", guessed_word)


if __name__ == "__main__":
    username = input(
        "If you want to play custom game from community, enter user username or pass: "
    ).strip()
    game = Game(username=username)
    asyncio.run(game.play_game())

