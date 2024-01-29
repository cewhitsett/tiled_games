from enum import Enum
from typing import Optional
import uuid
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import types
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import uuid

from games.twenty_forty_eight.game import Game, GameHelper

app = Flask(__name__, instance_relative_config=True)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///backend.db"


class Base(DeclarativeBase):
    """Base class for all models"""

    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class GameErrorCode(Enum):
    """Enum for game error codes"""

    GAME_NOT_FOUND = 1
    INVALID_GAME_UUID = 2


class GameError(Exception):
    """
    Base class for all game exceptions

    Attributes:
        error_code -- code for the error
        message -- explanation of the error
    """

    def __init__(self, error_code: GameErrorCode, message: str):
        self.error_code = error_code
        self.message = message
        super().__init__(self.message)


class GameModel2048(db.Model):
    """Model for 2048 game object"""

    id: Mapped[UUID] = mapped_column(types.Uuid, primary_key=True, default=uuid.uuid4)
    save_string: Mapped[str] = mapped_column(nullable=False)


class GameObject2048:
    """Object for 2048 game"""

    def __init__(self, game_uuid=None):
        self.game: Optional[Game] = None

        if game_uuid is None:
            self.game_uuid = uuid.uuid4()
        else:
            self.game_uuid = game_uuid

    def create_new_game(self):
        """Create a new game"""
        pass

    def load_game(self):
        """Loads a  game, given the game_uuid"""
        try:
            game_uuid = uuid.UUID(self.game_uuid)
        except ValueError as exc:
            raise GameError(
                GameErrorCode.INVALID_GAME_UUID, f"{self.game_uuid} is not a valid UUID"
            ) from exc

        with app.app_context():
            saved_game: Optional[GameModel2048] = GameModel2048.query.filter_by(
                id=game_uuid
            ).first()

            if saved_game is None:
                raise GameError(
                    GameErrorCode.GAME_NOT_FOUND,
                    f"Game with UUID {self.game_uuid} not found",
                )

            save_string = saved_game.save_string

            self.game = GameHelper.load(save_string)


with app.app_context():
    db.create_all()
