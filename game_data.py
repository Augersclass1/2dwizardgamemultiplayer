# =====================
# GAME VERSION
# =====================
GAMEVERSION = "1.1.0"

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
    },
    "gravel": {
        "id": 7,
        "name": "Gravel",
        "color": (128, 128, 128),
        "solid": True,
        "texture": "gravel"
    },
    "coal_ore": {
        "id": 8,
        "name": "Coal Ore",
        "color": (30, 30, 30),
        "solid": True,
        "texture": "coal_ore"
    },
    "copper_ore": {
        "id": 9,
        "name": "Copper Ore",
        "color": (177, 115, 66),
        "solid": True,
        "texture": "copper_ore"
    },
    "obsidian": {
        "id": 10,
        "name": "Obsidian",
        "color": (10, 10, 30),
        "solid": True,
        "texture": "obsidian"
    },
    "snow": {
        "id": 11,
        "name": "Snow",
        "color": (240, 248, 255),
        "solid": True,
        "texture": "snow"
    },
    "ice": {
        "id": 12,
        "name": "Ice",
        "color": (173, 216, 230),
        "solid": True,
        "texture": "ice"
    },
    "dark_oak_wood": {
        "id": 13,
        "name": "Dark Oak Wood",
        "color": (60, 40, 20),
        "solid": True,
        "texture": "dark_oak_wood"
    },
    "dark_oak_leaves": {
        "id": 14,
        "name": "Dark Oak Leaves",
        "color": (34, 85, 34),
        "solid": True,
        "texture": "dark_oak_leaves"
    },
    "cactus": {
        "id": 15,
        "name": "Cactus",
        "color": (34, 139, 34),
        "solid": True,
        "texture": "cactus"
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
    },
    "gravel_block": {
        "id": 7,
        "name": "Gravel Block",
        "block_id": 7,
        "action": "place_block"
    },
    "coal_ore_block": {
        "id": 8,
        "name": "Coal Ore Block",
        "block_id": 8,
        "action": "place_block"
    },
    "copper_ore_block": {
        "id": 9,
        "name": "Copper Ore Block",
        "block_id": 9,
        "action": "place_block"
    },
    "obsidian_block": {
        "id": 10,
        "name": "Obsidian Block",
        "block_id": 10,
        "action": "place_block"
    },
    "snow_block": {
        "id": 11,
        "name": "Snow Block",
        "block_id": 11,
        "action": "place_block"
    },
    "ice_block": {
        "id": 12,
        "name": "Ice Block",
        "block_id": 12,
        "action": "place_block"
    },
    "dark_oak_wood_block": {
        "id": 13,
        "name": "Dark Oak Wood Block",
        "block_id": 13,
        "action": "place_block"
    },
    "dark_oak_leaves_block": {
        "id": 14,
        "name": "Dark Oak Leaves Block",
        "block_id": 14,
        "action": "place_block"
    },
    "cactus_block": {
        "id": 15,
        "name": "Cactus Block",
        "block_id": 15,
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
GRAVEL_TILE = 7
COAL_ORE_TILE = 8
COPPER_ORE_TILE = 9
OBSIDIAN_TILE = 10
SNOW_TILE = 11
ICE_TILE = 12
DARK_OAK_WOOD_TILE = 13
DARK_OAK_LEAF_TILE = 14
CACTUS_TILE = 15
