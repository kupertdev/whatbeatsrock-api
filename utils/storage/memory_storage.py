#  THIS CLASS IS INITIALIZED IN the api/game.py file. IF YOU WANT TO USE MEMORY STORAGE TO WORK WITH API - INITIALIZE THE GAME CLASS

class MemoryStorage:
    def __init__(self):
        self.storage = {}

    def set(self, key: str, value: any):
        """Store a value with a specific key."""
        self.storage[key] = value

    def get(self, key: str, default: any = None) -> any:
        """Retrieve a value by key, return default if key is not found."""
        return self.storage.get(key, default)

    def delete(self, key: str):
        """Remove a value by key."""
        if key in self.storage:
            del self.storage[key]

    def clear(self):
        """Clear all stored values."""
        self.storage.clear()

    def __str__(self) -> str:
        return str(self.storage)