# logic/boss.py
import math
from config import ALLY, CLEAVER_RADIUS
from core.game_state import state


def update_boss_attack():
    if state.boss_state == "IDLE":
        state.boss_timer += 0.02
        if state.boss_timer > 3.0:
            state.boss_state = "WINDUP"
            state.boss_timer = 0.0

    elif state.boss_state == "WINDUP":
        state.boss_arm_angle -= 0.6
        if state.boss_arm_angle <= -85:
            state.boss_state = "SMASH"

    elif state.boss_state == "SMASH":
        state.boss_arm_angle += 5.5
        if state.boss_arm_angle >= 20 and not state.boss_did_damage:
            boss_smash_damage()

        if state.boss_arm_angle >= 35:
            state.boss_state = "COOLDOWN"
            state.boss_timer = 0.0

    elif state.boss_state == "COOLDOWN":
        state.boss_timer += 0.02
        if state.boss_timer > 2.0:
            state.boss_arm_angle = 0.0
            state.boss_state = "IDLE"
            state.boss_timer = 0.0
            state.boss_did_damage = False

    state.boss_arm_angle = max(-90.0, min(state.boss_arm_angle, 35.0))


def update_boss_rotation():
    if state.boss_state in ("SMASH", "COOLDOWN"):
        return

    closest_fighter = None
    min_dist = float("inf")

    for f in state.fighters:
        if f["state"] == ALLY and f["alive"]:
            dist = math.sqrt(f["x"]**2 + f["y"]**2)
            if dist < min_dist:
                min_dist = dist
                closest_fighter = f

    if closest_fighter is not None:
        target_angle = math.degrees(math.atan2(closest_fighter["y"], closest_fighter["x"])) + 90
        diff = target_angle - state.boss_facing_angle
        while diff > 180:
            diff -= 360
        while diff < -180:
            diff += 360
        state.boss_facing_angle += diff * 0.15


def boss_smash_damage():
    if state.boss_did_damage:
        return

    if state.allies_have_shield:
        state.shield_durability -= 1
        if state.shield_durability <= 0:
            state.allies_have_shield = False
        state.boss_did_damage = True
        return

    local_x, local_y = 95, -285
    theta = math.radians(state.boss_facing_angle)
    rot_x = local_x * math.cos(theta) - local_y * math.sin(theta)
    rot_y = local_x * math.sin(theta) + local_y * math.cos(theta)
    hit_x = state.boss_x + rot_x
    hit_y = state.boss_y + rot_y

    total_alive = sum(1 for f in state.fighters if f["state"] == ALLY and f["alive"])
    max_kills = int(math.ceil(total_alive * 0.2))

    victims = []
    for f in state.fighters:
        if not f["alive"] or f["state"] != ALLY:
            continue
        dist = math.sqrt((f["x"] - hit_x)**2 + (f["y"] - hit_y)**2)
        if dist <= CLEAVER_RADIUS:
            victims.append((dist, f))

    victims.sort(key=lambda v: v[0])
    for _, victim in victims[:max_kills]:
        victim["alive"] = False

    state.boss_did_damage = True