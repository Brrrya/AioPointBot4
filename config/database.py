from dataclasses import dataclass


@dataclass
class Database:
    """Configurate database connection"""
    db_name: str
    db_user: str
    db_password: str
    db_url: str
