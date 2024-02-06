"""
A module for generating maps, and the rules for generating them. It will be used
with wave function collapse to generate maps automatically
"""
from enum import Enum


class TileType(Enum):
    """
    Represents the type of a tile when generating
    """

    OCEAN = 0
    SAND = 1
    FOREST = 2
    STONE = 3
    GRASS = 4


class Tile:
    """
    Represents the smallest unit of a map, when generating
    """

    def __init__(self, tile_type: TileType, height: float = 0.0):
        self.tile_type = tile_type
        self.height = height


class TileRule:
    """
    Rules for which tiles can be placed next to each other. Normalizes the weights of the
    allowed neighbors to sum to 1, and fills in the missing neighbors with a weight of 0

    Args:
        tile_type (TileType): The root tile type
        allowed_neighbors (dict[TileType, float]): The allowed neighbors and their weights
    """

    def __init__(self, tile_type: TileType, allowed_neighbors: dict[TileType, float]):
        self.tile_type = tile_type
        self.neighbor_weights = allowed_neighbors

        weight_sum = sum(self.neighbor_weights.values())

        assert weight_sum > 0, "The sum of the weights must be greater than 0"

        for t_type in TileType:
            if t_type not in allowed_neighbors:
                self.neighbor_weights[t_type] = 0.0
            else:
                self.neighbor_weights[t_type] /= weight_sum


class TileRuleSet:
    """
    A set of rules for which tiles can be placed next to each other. Seems like
    the may need to be a reflexive rule for each tile type, but I'm not sure yet

    Args:
        rules (list[TileRule]): The rules for the tiles
    """

    def __init__(self, rules: list[dict[TileType, float]]):
        self.rules: dict[TileType, TileRule] = {rule.tile_type: rule for rule in rules}

    def get_rule(self, tile_type: TileType) -> TileRule:
        """
        Get the rule for a specific tile type

        Args:
            tile_type (TileType): The type of the tile

        Returns:
            TileRule: The rule for the tile type
        """
        return self.rules[tile_type]

    def get_allowed_neighbors(self, tile_type: TileType) -> list[TileType]:
        """
        Get the allowed neighbors for a specific tile type

        Args:
            tile_type (TileType): The type of the tile

        Returns:
            list[TileType]: The allowed neighbors and their weights
        """
        allowed = [
            tile_type
            for tile_type, weight in self.rules[tile_type].neighbor_weights.items()
            if weight > 0
        ]

        return allowed

    def is_allowed_neighbor(self, tile_type: TileType, neighbor_type: TileType) -> bool:
        """
        Check if a neighbor type is allowed for a specific tile type

        Args:
            tile_type (TileType): The type of the tile
            neighbor_type (TileType): The type of the neighbor

        Returns:
            bool: If the neighbor type is allowed
        """
        allowed_neighbors = self.get_allowed_neighbors(tile_type)
        return neighbor_type in allowed_neighbors

    def get_weight(self, tile_type: TileType, neighbor_type: TileType) -> float:
        """
        Get the weight of a neighbor type for a specific tile type

        Args:
            tile_type (TileType): The type of the tile
            neighbor_type (TileType): The type of the neighbor

        Returns:
            float: The weight of the neighbor type
        """
        return self.get_rule(tile_type).neighbor_weights[neighbor_type]


# Basic Rules for generating "islands",
# where ocean tiles can be next to sand tiles, and sand tiles being able
# to be next to any other tile type.
island_rules = [
    TileRule(
        TileType.OCEAN,
        {
            TileType.OCEAN: 1,
            TileType.SAND: 1,
        },
    ),
    TileRule(
        TileType.SAND,
        {
            TileType.OCEAN: 1,
            TileType.SAND: 1,
            TileType.FOREST: 1,
            TileType.GRASS: 1,
            TileType.STONE: 1,
        },
    ),
    TileRule(
        TileType.FOREST,
        {
            TileType.SAND: 1,
            TileType.FOREST: 1,
            TileType.GRASS: 1,
            TileType.STONE: 1,
        },
    ),
    TileRule(
        TileType.GRASS,
        {
            TileType.SAND: 1,
            TileType.FOREST: 1,
            TileType.GRASS: 1,
            TileType.STONE: 1,
        },
    ),
    TileRule(
        TileType.STONE,
        {
            TileType.SAND: 1,
            TileType.FOREST: 1,
            TileType.GRASS: 1,
            TileType.STONE: 1,
        },
    ),
]

ISLAND_RULESET = TileRuleSet(island_rules)
