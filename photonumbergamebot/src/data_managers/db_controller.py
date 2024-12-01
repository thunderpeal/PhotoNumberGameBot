from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

from photonumbergamebot.src.settings import DATABASE_URL

from .db_models import Base, GameState, PlayerStats


class DatabaseManager:
    def __init__(self, db_url):
        """
        Инициализация менеджера базы данных.
        :param db_url: URL подключения к базе данных.
        """
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self._create_tables()

    def _create_tables(self):
        """Создает таблицы в базе данных."""
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """Создает новую сессию."""
        return self.Session()

    # CRUD-операции для GameState
    def add_game_state(self, chat_id, number_to_find=1, who_found_last=""):
        with self.get_session() as session:
            game_state = GameState(
                chat_id=chat_id,
                number_to_find=number_to_find,
                who_found_last=who_found_last,
            )
            session.add(game_state)
            session.commit()

    def get_game_state(self, chat_id):
        with self.get_session() as session:
            return session.query(GameState).filter_by(chat_id=chat_id).first()

    def update_game_state(self, chat_id, new_number=None, user_name=None):
        with self.get_session() as session:
            game_state = session.query(GameState).filter_by(chat_id=chat_id).first()
            if game_state:
                if game_state.number_to_find != new_number:
                    game_state.number_to_find = new_number
                    game_state.who_found_last = user_name
                    session.commit()
            else:
                new_game = GameState(
                    chat_id=chat_id, number_to_find=new_number, who_found_last=user_name
                )
                session.add(new_game)
                session.commit()

    def add_player_stat(self, chat_id, player_name):
        with self.get_session() as session:
            player_stat = PlayerStats(
                chat_id=chat_id, player_name=player_name, found_numbers=1
            )
            session.add(player_stat)
            session.commit()

    def get_player_stats(self, chat_id):
        with self.get_session() as session:
            return (
                session.query(PlayerStats)
                .filter_by(chat_id=chat_id)
                .order_by(desc(PlayerStats.found_numbers))
                .all()
            )

    def update_player_stat(self, chat_id: str, player_name: str):
        with self.get_session() as session:
            player = (
                session.query(PlayerStats)
                .filter_by(chat_id=chat_id, player_name=player_name)
                .first()
            )
            if player:
                player.found_numbers += 1
                session.commit()
            else:
                self.add_player_stat(chat_id, player_name)

    def delete_player_stat(self, player_id):
        with self.get_session() as session:
            player_stat = session.query(PlayerStats).filter_by(id=player_id).first()
            if player_stat:
                session.delete(player_stat)
                session.commit()


db_manager = DatabaseManager(DATABASE_URL)
