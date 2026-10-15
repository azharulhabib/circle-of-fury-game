# input_handler.py
import os
from OpenGL.GLUT import *
from config import WINDOW_W, WINDOW_H
from core.game_state import state
from core.camera import camera
from logic.fighters import move_allies
from logic.weapons import check_hit_boss


def special_key_listener(key, x, y):
    # Left / Right arrows to choose when quit prompt is open
    if state.quit_dialog_open:
        if key == GLUT_KEY_LEFT:
            state.quit_selected_option = "NO"
            glutPostRedisplay()
        elif key == GLUT_KEY_RIGHT:
            state.quit_selected_option = "YES"
            glutPostRedisplay()
        return

    # Normal camera controls
    if key == GLUT_KEY_LEFT:
        camera.rotate(-3)
    elif key == GLUT_KEY_RIGHT:
        camera.rotate(3)
    elif key == GLUT_KEY_UP:
        camera.adjust_height(25)
    elif key == GLUT_KEY_DOWN:
        camera.adjust_height(-25)


def keyboard_listener(key, x, y):
    # When quit confirmation dialog is open
    if state.quit_dialog_open:
        # Enter confirms the selected option
        if key in (b'\r', b'\n'):
            if state.quit_selected_option == "YES":
                os._exit(0)
            else:
                state.quit_dialog_open = False
                glutPostRedisplay()
            return

        # Direct Y / N / ESC shortcuts
        if key in (b'y', b'Y'):
            os._exit(0)
        elif key in (b'n', b'N', b'\x1b'):
            state.quit_dialog_open = False
            glutPostRedisplay()
            return

        return  # Ignore other key presses while dialog is open

    # ESC opens the Quit confirmation prompt (q is disabled)
    if key == b'\x1b':
        state.quit_dialog_open = True
        state.quit_selected_option = "YES"
        glutPostRedisplay()
        return

    # R restarts the game
    if key in (b'r', b'R'):
        state.reset()
        glutPostRedisplay()
        return

    if state.game_over:
        return

    # C toggles cheat mode
    if key in (b'c', b'C'):
        state.cheat_mode = not state.cheat_mode

    # WASD ally movement
    step = 12
    if key in (b'w', b'W'):
        move_allies(0, step)
    elif key in (b's', b'S'):
        move_allies(0, -step)
    elif key in (b'a', b'A'):
        move_allies(-step, 0)
    elif key in (b'd', b'D'):
        move_allies(step, 0)


def mouse_listener(button, state_val, x, y):
    # Mouse clicks on YES / NO buttons in the quit dialog
    if state.quit_dialog_open:
        if button == GLUT_LEFT_BUTTON and state_val == GLUT_DOWN:
            gl_y = WINDOW_H - y
            box_h = 220
            by = (WINDOW_H - box_h) / 2
            bx = (WINDOW_W - 440) / 2

            # Click NO button
            if (bx + 70 <= x <= bx + 170) and (by + 80 <= gl_y <= by + 125):
                state.quit_dialog_open = False
                glutPostRedisplay()
                return

            # Click YES button
            if (bx + 250 <= x <= bx + 360) and (by + 80 <= gl_y <= by + 125):
                os._exit(0)
        return

    if state.game_over:
        return

    if button == GLUT_LEFT_BUTTON:
        if state_val == GLUT_DOWN:
            state.mouse_left_down = True
            state.last_mouse_x = x
            state.last_mouse_y = y
            if state.weapon_state == "READY":
                if check_hit_boss(x, y):
                    state.weapon_state = "ATTACKING"
        elif state_val == GLUT_UP:
            state.mouse_left_down = False

    elif button == GLUT_RIGHT_BUTTON and state_val == GLUT_DOWN:
        camera.toggle_first_person()