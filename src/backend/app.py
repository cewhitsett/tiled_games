import uuid
from enum import Enum
from typing import Optional

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import types
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.games.twenty_forty_eight.game import (
    Game,
    GameConfig,
    GameHelper,
    SlideDirection,
    SlideResult,
)

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

    def __init__(
        self, game_uuid: Optional[str] = None, config: Optional[GameConfig] = None
    ):
        # Passing in a game config will only make sense if we are creating a new game,

        # These will be set within the constructor helper methods,
        # so we don't need to worry about them being None
        self.game: Game = None
        self.game_uuid: str = None

        if config:
            self.config: GameConfig = config
        else:
            self.config: GameConfig = GameConfig()

        if game_uuid is None:
            self.create_new_game()
        else:
            self.game_uuid = game_uuid
            self.load_game()

    def create_new_game(self):
        """Creates a new game"""
        self.game = Game(self.config)
        self.game_uuid = uuid.uuid4()
        save_string = self.game.to_json()

        with app.app_context():
            game_model = GameModel2048(id=self.game_uuid, save_string=save_string)
            db.session.add(game_model)
            db.session.commit()

    def save_game(self):
        """
        Saves the game to the database, creating a new entry if one does not exist
        """
        with app.app_context():
            save_string = self.game.to_json()
            prev_game_model = db.session.execute(
                db.select(GameModel2048).where(GameModel2048.id == self.game_uuid)
            ).scalar_one()

            if prev_game_model is None:
                raise GameError(
                    GameErrorCode.GAME_NOT_FOUND,
                    f"Critical Error: {self.game_uuid} invalid while attempting to save game",
                )

            prev_game_model.save_string = save_string
            db.session.add(prev_game_model)
            db.session.commit()

    def load_game(self):
        """Loads a  game, given the game_uuid"""
        try:
            if isinstance(self.game_uuid, str):
                game_uuid = uuid.UUID(self.game_uuid)
            else:
                game_uuid = self.game_uuid
        except ValueError as exc:
            raise GameError(
                GameErrorCode.INVALID_GAME_UUID, f"{self.game_uuid} is not a valid UUID"
            ) from exc

        with app.app_context():
            saved_game: Optional[GameModel2048] = db.session.execute(
                db.select(GameModel2048).where(GameModel2048.id == game_uuid)
            ).scalar_one()

            if saved_game is None:
                raise GameError(
                    GameErrorCode.GAME_NOT_FOUND,
                    f"Game with UUID {self.game_uuid} not found",
                )

            save_string = saved_game.save_string

            self.game = GameHelper.load(save_string)


@app.route("/perform_slide/v1", methods=["POST"])
def perform_slide():
    """
    Perform a slide, given a slide direction and game UUID

    Parameters:
        - slide_direction: The direction to slide the tiles, one of "up", "down", "left", "right" (Representative SlideDirection enum names)
        - game_uuid: The UUID of the game to slide, provided originally when the client created the game


    Responses:
        - 200: Slide was successful
        - 400: Bad request, something was probably malformed
        - 500: Error processing slide

    Response JSON:
        - result: The result of the slide, one of "normal" or "game_over"
        - reason: The reason for the result, one of "win", "board_full", "spawn_kill", "spawn_fill".
        - game: The game state after the slide
    """
    slide_direction: str = request.form.get("slide_direction", type=str, default="")
    game_uuid: str = request.form.get("game_uuid", type=str, default="")

    if not slide_direction:
        return jsonify({"error": "No slide direction provided"}), 400

    if not game_uuid:
        return jsonify({"error": "No game UUID provided"}), 400

    try:
        game_uuid = uuid.UUID(game_uuid)
    except ValueError:
        return jsonify({"error": f"{game_uuid} is not a valid UUID"}), 400

    if slide_direction not in ["up", "down", "left", "right"]:
        return (
            jsonify({"error": f"{slide_direction} is not a valid slide direction"}),
            400,
        )

    slide_direction: SlideDirection = SlideDirection[slide_direction.upper()]
    game_object = GameObject2048(game_uuid)

    if not game_object.game.can_play():
        return jsonify({"error": "Game is over"}), 400

    result: SlideResult = game_object.game.play_turn(slide_direction)
    game_object.save_game()

    win_score = game_object.game.config.win_tile_value
    if game_object.game.get_highest_tile() >= win_score:
        return (
            jsonify(
                {
                    "result": "game_over",
                    "reason": "win",
                    "game": game_object.game.to_dict(),
                }
            ),
            200,
        )

    if result in [SlideResult.NORMAL, SlideResult.SPAWN_FILL]:
        return (
            jsonify(
                {
                    "result": "normal",
                    "reason": result.name,
                    "game": game_object.game.to_dict(),
                }
            ),
            200,
        )

    if result in [SlideResult.BOARD_FULL, SlideResult.SPAWN_KILL]:
        if game_object.game.config.spawn_kill:
            return (
                jsonify(
                    {
                        "result": "game_over",
                        "reason": result.name,
                        "game": game_object.game.to_dict(),
                    }
                ),
                200,
            )

    return jsonify({"error": "Could not resolve slide result"}), 500


@app.route("/", methods=["GET"])
@app.route("/create_game/v1", methods=["POST"])
def create_game():
    """
    Creates a new game, provided the desired config fields. Each field
    is optional, and will defaut to reasonable 2048 defaults

    Parameters:
        - grid_size: The width and height of the game grid. Defaults to 4
        - spawn_tile_count: The number of tiles to spawn after a slide. Defaults to 2
        - starting_tile_count: The number of tiles to start the game with. Defaults to 2
        - win_tile_value: The value of the tile that wins the game. Defaults to 2048
        - mutation_probability: (float) The probability of a tile mutation. Defaults to 0.1
        - mutation_at_start: (bool) Whether the starting tiles can be mutated. Defaults to True
        - spawn_kill: (bool) Whether to end the game if a spawn is not possible. Defaults to False
        - root_tile_value: The value of the root tile. Defaults to 2

    Responses:
        - 200: Game was created successfully
        - 500: Error creating game

    Response JSON:
        - game_uuid: The UUID of the game that was created
        - game: The game state after the slide
    """
    grid_size: int = request.args.get("grid_size", type=int, default=4)
    spawn_tile_count: int = request.args.get("spawn_tile_count", type=int, default=2)
    starting_tile_count: int = request.args.get(
        "starting_tile_count", type=int, default=2
    )
    win_tile_value: int = request.args.get("win_tile_value", type=int, default=2048)
    mutation_probability: float = request.args.get(
        "mutation_probability", type=float, default=0.1
    )
    mutation_at_start: bool = request.args.get(
        "mutation_at_start", type=bool, default=True
    )
    spawn_kill: bool = request.args.get("spawn_kill", type=bool, default=False)
    root_tile_value: int = request.args.get("root_tile_value", type=int, default=2)

    game_config = GameConfig(
        grid_size=grid_size,
        spawn_tile_count=spawn_tile_count,
        starting_tile_count=starting_tile_count,
        win_tile_value=win_tile_value,
        mutation_probability=mutation_probability,
        mutation_at_start=mutation_at_start,
        spawn_kill=spawn_kill,
        root_tile_value=root_tile_value,
    )

    game_object = GameObject2048(config=game_config)
    game_object.create_new_game()

    return (
        jsonify(
            {"game_uuid": game_object.game_uuid, "game": game_object.game.to_dict()}
        ),
        200,
    )


@app.route("/get_game/v1", methods=["GET"])
def get_game():
    """
    Returns the game state, given a game UUID

    Parameters:
        - game_uuid: The UUID of the game to retrieve

    Responses:
        - 200: Game was retrieved successfully
        - 400: Bad request, something was probably malformed

    Response JSON:
        - game: The game state
    """
    game_uuid: str = request.args.get("game_uuid", type=str, default="")

    if not game_uuid:
        return jsonify({"error": "No game UUID provided"}), 400

    try:
        game_uuid = uuid.UUID(game_uuid)
    except ValueError:
        return jsonify({"error": f"{game_uuid} is not a valid UUID"}), 400

    game_object = GameObject2048(game_uuid)
    return jsonify({"game": game_object.game.to_dict()}), 200


with app.app_context():
    db.create_all()
