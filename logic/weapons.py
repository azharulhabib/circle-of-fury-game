# logic/weapons.py
import math
import random
from config import (
    WINDOW_W, WINDOW_H, SPEAR_DAMAGE, BULLET_DAMAGE,
    MAX_ATTACK_DAMAGE, ALLY
)
from core.game_state import state


def check_hit_boss(mx, my):
    center_x = WINDOW_W / 2
    center_y = WINDOW_H / 2
    box_width = 300
    box_height = 550
    return abs(mx - center_x) < (box_width / 2) and abs(my - center_y) < (box_height / 2)


def update_weapons():
    if state.allies_have_gun and state.mouse_left_down and state.weapon_state == "READY":
        if check_hit_boss(state.last_mouse_x, state.last_mouse_y):
            state.weapon_state = "ATTACKING"

    if state.weapon_state == "ATTACKING":
        speed = 0.1 if state.allies_have_gun else 0.01
        state.weapon_anim_t += speed

        if state.weapon_anim_t >= 1.0:
            ally_count = sum(1 for f in state.fighters if f["state"] == ALLY and f["alive"])
            damage_per_unit = BULLET_DAMAGE if state.allies_have_gun else SPEAR_DAMAGE
            damage = min(ally_count * damage_per_unit, MAX_ATTACK_DAMAGE)

            state.boss_hp -= damage
            if state.boss_hp <= 0:
                state.boss_hp = 0
                state.game_over = True

            # Floating text spawns
            for _ in range(ally_count):
                state.damage_texts.append({
                    "text": f"-{damage_per_unit}",
                    "x": state.boss_x + random.uniform(-40, 40),
                    "y": state.boss_y + random.uniform(-40, 40),
                    "z": state.boss_z + random.uniform(260, 320),
                    "life": 1.0
                })

            if state.allies_have_gun:
                state.gun_ammo -= 1
                if state.gun_ammo <= 0:
                    state.allies_have_gun = False
                state.weapon_cooldown = 0.2
            else:
                state.weapon_cooldown = 1.0

            state.weapon_state = "COOLDOWN"
            state.weapon_anim_t = 0.0

            # Drop spawning logic every 4 attacks
            if not state.allies_have_gun:
                state.attack_count += 1
                if state.attack_count >= 4:
                    angle = random.randint(0, 360)
                    r = 250
                    px = r * math.cos(math.radians(angle))
                    py = r * math.sin(math.radians(angle))

                    if state.next_drop_is_gun:
                        if not state.gun_active and not state.allies_have_gun:
                            state.gun_active = True
                            state.gun_pos = [px, py]
                            state.next_drop_is_gun = False
                    else:
                        if not state.shield_active and not state.allies_have_shield:
                            state.shield_active = True
                            state.shield_pos = [px, py]
                            state.next_drop_is_gun = True
                    state.attack_count = 0

    elif state.weapon_state == "COOLDOWN":
        state.weapon_cooldown -= 0.02
        if state.weapon_cooldown <= 0:
            state.weapon_state = "READY"