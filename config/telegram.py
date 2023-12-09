from dataclasses import dataclass


@dataclass
class TgBot:
    """Configurate telegram connection, append token"""
    token: str
