# Circle of Fury: 3D Boss Arena

A real-time, squad-based 3D combat simulation developed using Python and PyOpenGL (GLUT/GLU). 

The application implements a complete graphics and game pipeline from the ground up without third-party game engines or external 3D asset loaders. All geometry, character hierarchies, animation cycles, lighting, and collision mathematics are computed and rendered procedurally.

---

## Overview

Players command an infantry squad in a circular arena against a towering, multi-jointed boss entity. The objective is to navigate the arena, recruit neutral units to scale attack damage, acquire dynamic equipment drops, and defeat the central boss while managing positioning to avoid lethal area-of-effect cleaver strikes.

---

## Technical Highlights

### 1. Procedural 3D Graphics Pipeline
* **Native OpenGL Rendering:** All models (boss entity, humanoid fighters, weapons, and arena colosseum) are generated procedurally using OpenGL primitives (`GL_TRIANGLES`, `GL_QUADS`), matrix stacks (`glPushMatrix`, `glPopMatrix`), and hierarchical transformations (`glTranslatef`, `glRotatef`, `glScalef`).
* **Dual-Mode Camera System:** Features a configurable spherical coordinate orbit camera (360-degree rotation and elevation control via `gluLookAt`) and an interactive first-person perspective locked directly to the squad commander.
* **Hybrid 2D/3D Projection:** Implements an orthographic overlay (`gluOrtho2D`) decoupled from the 3D perspective pipeline to render real-time health bars, floating damage numbers, and interactive user prompts.

### 2. Entity State Machine and Boss AI
* **Finite State Machine (FSM):** The boss operates on a deterministic attack cycle (`IDLE` -> `WINDUP` -> `SMASH` -> `COOLDOWN`) with variable animation interpolation.
* **Dynamic Target Tracking:** In non-attack phases, the boss calculates angular displacement toward the nearest ally and continuously aligns its forward vector via smooth interpolation.
* **Rotational Hitbox Mathematics:** Cleaver impacts compute transformed world-space coordinates from local joint matrices to evaluate radial area-of-effect damage against the player squad.

### 3. Squad and Combat Mechanics
* **Dynamic Unit Recruitment:** Proximity-based collision detection converts neutral perimeter units into active allies, dynamically scaling squad damage output.
* **Tiered Weaponry and Inventory:**
  * **Spear:** Baseline weapon with synchronized thrust and projectile animations.
  * **Firearm:** High-velocity projectile class with ammo constraints and rapid cooldowns.
  * **Shield:** Finite-durability defensive gear that completely negates boss smash damage.
* **Autonomous Navigation (Cheat Mode):** Includes an autonomous vector pathfinding mode that guides the squad toward the nearest neutral recruit.

---

## Controls

| Input | Function |
| :--- | :--- |
| **W, A, S, D** | Move active squad across the arena floor |
| **Left Mouse Click** *(on Boss)* | Command squad attack (Spear or Firearm) |
| **Right Mouse Click** | Toggle between Orbit and First-Person camera |
| **Arrow Left / Right** | Orbit camera horizontally around the arena |
| **Arrow Up / Down** | Adjust camera height and vertical angle |
| **C** | Toggle autonomous pathfinding mode |
| **R** | Reset simulation state |
| **ESC** | Open pause and exit confirmation modal |

---

## Architecture

The project adheres to a modular architecture separating state management, graphics rendering, and gameplay logic:

```text
circle-of-fury-game/
|
|-- main.py              # Application entry point and GLUT lifecycle hooks
|-- config.py            # Global constants, physics parameters, and dimensions
|-- input_handler.py     # Keyboard, mouse, and special key event dispatchers
|
|-- core/
|   |-- game_state.py    # Encapsulated state singleton
|   `-- camera.py        # Projection setup, orbit math, and first-person view
|
|-- graphics/
|   |-- models.py        # Procedural 3D OpenGL primitives and character assemblies
|   `-- ui.py            # 2D Orthographic HUD, damage indicators, and dialogs
|
`-- logic/
    |-- boss.py          # Boss state machine, orientation, and damage calculations
    |-- fighters.py      # Squad movement, boundary checking, and recruitment
    `-- weapons.py       # Weapon cooldowns, projectile trajectories, and drop spawns
```

---

## Installation and Execution

### Requirements
* Python 3.9 or higher
* PyOpenGL and PyOpenGL_accelerate

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/azharulhabib/circle-of-fury-game.git
   cd circle-of-fury-game
   ```

2. **Initialize a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the game:**
   ```bash
   python main.py
   ```

---