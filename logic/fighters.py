# logic/fighters.py
import math
from config import INNER_RADIUS, OUTER_RADIUS, ALLY, IDLE
from core.game_state import state


def can_move_to(x, y):
    r = math.sqrt(x*x + y*y)
    return (INNER_RADIUS + 15) < r < (OUTER_RADIUS - 15)


def move_allies(dx, dy, phase_speed=8):
    for f in state.fighters:
        if f["state"] == ALLY:
            f["moving"] = False

    any_moved = False
    for f in state.fighters:
        if f["state"] == ALLY and f["alive"]:
            nx = f["x"] + dx
            ny = f["y"] + dy
            if can_move_to(nx, ny):
                f["x"] = nx
                f["y"] = ny
                f["moving"] = True
                any_moved = True

    if any_moved:
        state.walk_phase += phase_speed


def check_ally_conversion():
    for f in state.fighters:
        if f["state"] != ALLY or not f["alive"]:
            continue

        for other in state.fighters:
            if other["state"] == IDLE and other["alive"]:
                dist = math.sqrt((f["x"] - other["x"])**2 + (f["y"] - other["y"])**2)
                if dist < 22:
                    other["state"] = ALLY
                    other["moving"] = False
                    if "spawn_id" in other:
                        s_id = other["spawn_id"]
                        state.spawn_points[s_id]["timer"] = 30.0
                        del other["spawn_id"]

        if state.shield_active:
            dist = math.sqrt((f["x"] - state.shield_pos[0])**2 + (f["y"] - state.shield_pos[1])**2)
            if dist < 30:
                state.shield_active = False
                state.allies_have_shield = True
                state.allies_have_gun = False
                state.shield_durability = 3

        if state.gun_active:
            dist = math.sqrt((f["x"] - state.gun_pos[0])**2 + (f["y"] - state.gun_pos[1])**2)
            if dist < 30:
                state.gun_active = False
                state.allies_have_gun = True
                state.allies_have_shield = False
                state.gun_ammo = 20


def update_spawns():
    for i, sp in enumerate(state.spawn_points):
        if sp["timer"] > 0:
            sp["timer"] -= 0.02
            if sp["timer"] <= 0:
                state.fighters.append({
                    "x": sp["x"], "y": sp["y"],
                    "state": IDLE, "alive": True, "moving": False, "spawn_id": i
                })
                sp["timer"] = 0


def update_cheat_movement():
    if not state.cheat_mode or state.game_over:
        return

    ref_ally = next((f for f in state.fighters if f["state"] == ALLY and f["alive"]), None)
    if not ref_ally:
        return

    closest_idle = None
    min_dist = float("inf")
    for f in state.fighters:
        if f["state"] == IDLE and f["alive"]:
            dist = math.sqrt((f["x"] - ref_ally["x"])**2 + (f["y"] - ref_ally["y"])**2)
            if dist < min_dist:
                min_dist = dist
                closest_idle = f

    if closest_idle:
        dir_x = closest_idle["x"] - ref_ally["x"]
        dir_y = closest_idle["y"] - ref_ally["y"]
        length = math.sqrt(dir_x**2 + dir_y**2)
        if length > 0:
            speed = 0.8
            move_allies((dir_x / length) * speed, (dir_y / length) * speed, 3)