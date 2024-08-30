import uuid
import secrets

class IDGenerator:
    @staticmethod
    def generate_uuid_v4() -> str:
        return str(uuid.uuid4())
    
    @staticmethod
    def generate_uuid_bytes() -> bytes:
        """
        Deprecated. Use generate_uuid_v4
        """
        random_bytes = secrets.token_bytes(16)
        random_bytes = bytearray(random_bytes)
        random_bytes[6] = (random_bytes[6] & 0x0f) | 0x40
        random_bytes[8] = (random_bytes[8] & 0x3f) | 0x80
        return bytes(random_bytes)

    @staticmethod
    def format_uuid_bytes_to_string(uuid_bytes: bytes) -> str:
        return str(uuid.UUID(bytes=uuid_bytes))
