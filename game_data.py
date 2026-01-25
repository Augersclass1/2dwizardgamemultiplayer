# =====================
# BLOCK DEFINITIONS
# =====================
BLOCKS = {
    "air": {
        "id": 0,
        "name": "Air",
        "color": (255, 255, 255),
        "solid": False,
        "texture": None
    },
    "dirt": {
        "id": 1,
        "name": "Dirt",
        "color": (139, 69, 19),
        "solid": True,
        "texture": "dirt"
    },
    "stone": {
        "id": 2,
        "name": "Stone",
        "color": (110, 110, 110),
        "solid": True,
        "texture": "stone"
    },
    "grass": {
        "id": 3,
        "name": "Grass",
        "color": (34, 139, 34),
        "solid": True,
        "texture": "grass"
    },
    "sand": {
        "id": 4,
        "name": "Sand",
        "color": (194, 178, 128),
        "solid": True,
        "texture": "sand"
    },
    "wood": {
        "id": 5,
        "name": "Wood",
        "color": (101, 67, 33),
        "solid": True,
        "texture": "wood"
    },
    "leaves": {
        "id": 6,
        "name": "Leaves",
        "color": (50, 205, 50),
        "solid": True,
        "texture": "leaves"
    }
}

# =====================
# ITEM DEFINITIONS
# =====================
ITEMS = {
    "dirt_block": {
        "id": 1,
        "name": "Dirt Block",
        "block_id": 1,
        "action": "place_block"
    },
    "stone_block": {
        "id": 2,
        "name": "Stone Block",
        "block_id": 2,
        "action": "place_block"
    },
    "grass_block": {
        "id": 3,
        "name": "Grass Block",
        "block_id": 3,
        "action": "place_block"
    },
    "sand_block": {
        "id": 4,
        "name": "Sand Block",
        "block_id": 4,
        "action": "place_block"
    },
    "wood_block": {
        "id": 5,
        "name": "Wood Block",
        "block_id": 5,
        "action": "place_block"
    },
    "leaves_block": {
        "id": 6,
        "name": "Leaves Block",
        "block_id": 6,
        "action": "place_block"
    }
}

# =====================
# BLOCK ID CONSTANTS
# =====================
AIR = 0
DIRT_TILE = 1
STONE_TILE = 2
GRASS_TILE = 3
SAND_TILE = 4
WOOD_TILE = 5
LEAF_TILE = 6
