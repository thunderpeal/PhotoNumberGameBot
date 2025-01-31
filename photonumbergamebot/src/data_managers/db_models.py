from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class GameState(Base):
    __tablename__ = "game_state"
    chat_id = Column(String, primary_key=True, unique=True, nullable=False)
    number_to_find = Column(Integer, default=1)
    who_found_last = Column(String, nullable=False)


class PlayerStats(Base):
    __tablename__ = "player_stats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String, nullable=False)
    player_name = Column(String, nullable=False)
    found_numbers = Column(Integer, default=0)


class PaymentLinkStats(Base):
    __tablename__ = "payment_link_stats"
    chat_id = Column(String, primary_key=True, unique=True, nullable=False)
    payment_link_counter = Column(Integer, default=0)
