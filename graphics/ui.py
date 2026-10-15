# graphics/ui.py
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_HELVETICA_18
from config import WINDOW_W, WINDOW_H, ALLY, IDLE
from core.game_state import state


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_W, 0, WINDOW_H)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_health_bar():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_W, 0, WINDOW_H)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)

    bar_width = 400
    bar_height = 20
    x = (WINDOW_W - bar_width) / 2
    y = WINDOW_H - 40

    # Red background
    glColor3f(0.5, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + bar_width, y)
    glVertex2f(x + bar_width, y + bar_height)
    glVertex2f(x, y + bar_height)
    glEnd()

    # Green remaining HP
    current_hp = max(0, state.boss_hp)
    current_width = bar_width * (current_hp / 1000.0)

    if current_width > 0:
        glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + current_width, y)
        glVertex2f(x + current_width, y + bar_height)
        glVertex2f(x, y + bar_height)
        glEnd()

    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_floating_damage():
    glDisable(GL_DEPTH_TEST)
    for dt in state.damage_texts:
        glColor3f(1.0, 0.0, 0.0)
        glRasterPos3f(dt["x"], dt["y"], dt["z"])
        for ch in dt["text"]:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
    glEnable(GL_DEPTH_TEST)


def update_damage_texts():
    to_keep = []
    for dt in state.damage_texts:
        dt["z"] += 2.0
        dt["life"] -= 0.02
        if dt["life"] > 0:
            to_keep.append(dt)
    state.damage_texts = to_keep


def draw_quit_dialog():
    if not state.quit_dialog_open:
        return

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_W, 0, WINDOW_H)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)

    # Dark background box
    box_w, box_h = 440, 220
    bx = (WINDOW_W - box_w) / 2
    by = (WINDOW_H - box_h) / 2

    glColor3f(0.12, 0.12, 0.15)
    glBegin(GL_QUADS)
    glVertex2f(bx, by)
    glVertex2f(bx + box_w, by)
    glVertex2f(bx + box_w, by + box_h)
    glVertex2f(bx, by + box_h)
    glEnd()

    # Border outline
    glColor3f(0.8, 0.8, 0.2)
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
    glVertex2f(bx, by)
    glVertex2f(bx + box_w, by)
    glVertex2f(bx + box_w, by + box_h)
    glVertex2f(bx, by + box_h)
    glEnd()

    # Title text
    draw_text(bx + 110, by + 160, "DO YOU WANT TO QUIT?")

    # Buttons: NO on left, YES on right
    if state.quit_selected_option == "NO":
        glColor3f(0.9, 0.2, 0.2)
        draw_text(bx + 85, by + 95, "> [ NO ] <")
    else:
        glColor3f(0.5, 0.5, 0.5)
        draw_text(bx + 100, by + 95, "[ NO ]")

    if state.quit_selected_option == "YES":
        glColor3f(0.2, 0.9, 0.3)
        draw_text(bx + 265, by + 95, "> [ YES ] <")
    else:
        glColor3f(0.5, 0.5, 0.5)
        draw_text(bx + 280, by + 95, "[ YES ]")

    draw_text(bx + 55, by + 35, "Arrow Keys to select, ENTER to confirm")

    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_hud(camera_first_person):
    draw_health_bar()
    draw_floating_damage()

    draw_text(10, WINDOW_H - 30, "Boss Arena: Circle of Fury")
    draw_text(10, WINDOW_H - 60, f"Boss HP: {state.boss_hp}")

    # Separated ally and recruit counts so it correctly says 0 on defeat
    ally_count = sum(1 for f in state.fighters if f["state"] == ALLY and f["alive"])
    idle_count = sum(1 for f in state.fighters if f["state"] == IDLE and f["alive"])
    draw_text(10, WINDOW_H - 90, f"Allies: {ally_count} | Recruits: {idle_count}")

    msg = f"Weapon: {'Gun (Ammo: ' + str(state.gun_ammo) + ')' if state.allies_have_gun else 'Spear'}"
    if state.weapon_state == "COOLDOWN":
        msg += " (Cooldown)"
    draw_text(10, WINDOW_H - 120, msg)

    draw_text(10, WINDOW_H - 150, f"Cheat Mode (C): {'ON' if state.cheat_mode else 'OFF'}")

    if state.allies_have_shield:
        draw_text(10, WINDOW_H - 180, f"SHIELD ACTIVE! Blocks Left: {state.shield_durability}")

    if state.game_over:
        if state.boss_hp <= 0:
            draw_text(WINDOW_W // 2 - 80, WINDOW_H // 2, "VICTORY! BOSS SLAIN")
        else:
            draw_text(WINDOW_W // 2 - 50, WINDOW_H // 2, "GAME OVER")
        draw_text(WINDOW_W // 2 - 70, WINDOW_H // 2 - 30, "Press R to Restart")

    # Draw quit dialog on top if open
    draw_quit_dialog()