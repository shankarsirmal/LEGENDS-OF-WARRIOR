# Sprite sheet grid layout (columns, rows) per character and level
SPRITE_LAYOUTS = {
    "warrior": {
        1: (5, 4),  # Level 1 → 5 cols × 4 rows
        2: (5, 5),  # Level 2 → 5 cols × 5 rows
        3: (5, 5)   # Level 3 → 5 cols × 5 rows
    },
    "monster": {
        1: (6, 5),  # Level 1 → 6 cols × 5 rows
        2: (5, 5),  # Level 2 → 5 cols × 5 rows
        3: (5, 6)   # Level 3 → 5 cols × 6 rows
    }
}
