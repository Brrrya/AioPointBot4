from dataclasses import dataclass


@dataclass
class Redis_DB:
    """Configurate redis connection"""
    db_host: str
    db_port: int
    db_password: str
    db_num: int
    db_url: str

