SPRITE_LAYOUTS = {
    "warrior": {
        1: {"columns": 5, "rows": 4, "actions": ["idle", "run", "attack", "die"], "frames_per_row": [5, 5, 5, 5]},
        2: {"columns": 5, "rows": 5, "actions": ["idle", "run", "run_sword", "attack", "die"], "frames_per_row": [5, 5, 4, 3, 5]},
        3: {"columns": 5, "rows": 5, "actions": ["idle", "run", "move_enemy", "attack", "die"], "frames_per_row": [5, 5, 5, 5, 5]}
    },
    "monster": {
        1: {"columns": 6, "rows": 5, "actions": ["idle", "act", "attack1", "attack2", "die"], "frames_per_row": [6, 6, 6, 6, 6]},
        2: {"columns": 5, "rows": 5, "actions": ["idle", "act", "attack1", "attack2", "die"], "frames_per_row": [5, 5, 5, 4, 5]},
        3: {"columns": 5, "rows": 5, "actions": ["idle", "move", "attack1", "attack2", "die"], "frames_per_row": [5, 5, 5, 5, 5]}
    }
}
