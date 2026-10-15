# main.py
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import gluNewQuadric

from config import WINDOW_W, WINDOW_H, ALLY
from core.game_state import state
from core.camera import camera
from graphics.models import (
    draw_arena, draw_boss, draw_fighters,
    draw_shield_model, draw_gun_model
)
from graphics.ui import draw_hud, update_damage_texts
from logic.boss import update_boss_attack, update_boss_rotation
from logic.fighters import check_ally_conversion, update_spawns, update_cheat_movement
from logic.weapons import update_weapons
from input_handler import special_key_listener, keyboard_listener, mouse_listener


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, WINDOW_W, WINDOW_H)

    camera.setup()
    draw_arena()

    if state.shield_active:
        glPushMatrix()
        glTranslatef(state.shield_pos[0], state.shield_pos[1], 30)
        glRotatef(90, 1, 0, 0)
        draw_shield_model()
        glPopMatrix()

    if state.gun_active:
        glPushMatrix()
        glTranslatef(state.gun_pos[0], state.gun_pos[1], 10)
        glRotatef(90, 1, 0, 0)
        draw_gun_model()
        glPopMatrix()

    draw_boss()
    draw_fighters()
    draw_hud(camera.first_person)

    glutSwapBuffers()


def idle():
    # Pause updates while the quit confirmation dialog is open
    if state.quit_dialog_open:
        glutPostRedisplay()
        return

    ally_count = sum(1 for f in state.fighters if f["state"] == ALLY and f["alive"])
    if ally_count == 0:
        state.game_over = True

    if state.game_over:
        glutPostRedisplay()
        return

    update_boss_attack()
    update_boss_rotation()
    check_ally_conversion()
    update_spawns()
    update_weapons()
    update_damage_texts()
    update_cheat_movement()
    glutPostRedisplay()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_W, WINDOW_H)
    glutInitWindowPosition(50, 50)
    glutCreateWindow(b"Boss Arena: Circle of Fury")

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.266, 0.765, 0.996, 1.0)
    state.quadric = gluNewQuadric()

    glutDisplayFunc(display)
    glutSpecialFunc(special_key_listener)
    glutKeyboardFunc(keyboard_listener)
    glutMouseFunc(mouse_listener)
    glutIdleFunc(idle)
    glutMainLoop()


if __name__ == "__main__":
    main()