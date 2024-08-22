from dataclasses import dataclass

@dataclass
class ApiEndpoints:
    api_vs: str = "https://www.whatbeatsrock.com/api/vs"
    game_info: str = "https://www.whatbeatsrock.com/api/users/{user_id}/custom"
    user_info: str = "https://www.whatbeatsrock.com/api/users?handle={username}"