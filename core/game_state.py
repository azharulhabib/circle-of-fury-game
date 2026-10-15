# core/game_state.py
import math
from config import (
    BOSS_INITIAL_HP,
    ALLY,
    IDLE,
    ARM_LENGTH,
)


class GameState:
    def __init__(self):
        self.quadric = None
        self.reset()

    def reset(self):
        # Boss state
        self.boss_x = 0.0
        self.boss_y = 0.0
        self.boss_z = 0.0
        self.boss_hp = BOSS_INITIAL_HP
        self.boss_state = "IDLE"
        self.boss_timer = 0.0
        self.boss_arm_angle = 0.0
        self.arm_length = ARM_LENGTH
        self.boss_arm_dir = 1
        self.boss_did_damage = False
        self.boss_facing_angle = 0.0

        # Game lifecycle
        self.game_over = False
        self.cheat_mode = False

        # Quit confirmation dialog
        self.quit_dialog_open = False
        self.quit_selected_option = "YES"  # "YES" or "NO"

        # Weapon system
        self.weapon_state = "READY"
        self.weapon_anim_t = 0.0
        self.weapon_cooldown = 0.0
        self.attack_count = 0
        self.next_drop_is_gun = True

        # Shield
        self.shield_active = False
        self.shield_pos = [0.0, 0.0]
        self.allies_have_shield = False
        self.shield_durability = 0

        # Gun
        self.gun_active = False
        self.gun_pos = [0.0, 0.0]
        self.allies_have_gun = False
        self.gun_ammo = 0

        # Mouse
        self.mouse_left_down = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0

        # Animation & entities
        self.walk_phase = 0.0
        self.damage_texts = []
        self.fighters = []
        self.spawn_points = []
        self.init_fighters()

    def init_fighters(self):
        self.fighters = []
        self.spawn_points = []
        self.damage_texts = []

        # Initial 6 ally fighters
        for i in range(6):
            self.fighters.append({
                "x": -200 + i * 15,
                "y": 150,
                "state": ALLY,
                "alive": True,
                "moving": False
            })

        # 14 neutral fighters around perimeter
        for i in range(14):
            angle_deg = i * (360 / 14)
            r = 320
            fx = r * math.cos(math.radians(angle_deg))
            fy = r * math.sin(math.radians(angle_deg))

            self.spawn_points.append({
                "x": fx,
                "y": fy,
                "timer": 0.0
            })

            self.fighters.append({
                "x": fx,
                "y": fy,
                "state": IDLE,
                "alive": True,
                "moving": False,
                "spawn_id": i
            })


# Global singleton instance
state = GameState()