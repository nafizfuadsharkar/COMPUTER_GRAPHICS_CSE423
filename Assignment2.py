from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import time

# Constants
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500

# Game Variables
r = 10  # Radius for projectiles
shooter_x = SCREEN_WIDTH // 2
shooter_y = r
exit_game = False
speed = 0.4
max_miss = 3
max_misfire = 3
misfire = 0
score = 0
game_over = False
pause = False
last_frame_time = time.time()

# Button areas
restart_area = (30, SCREEN_HEIGHT - 50)
pause_play_area = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
cross_area = (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50)

# Active objects
falling_circles = []  # Format: [x, y, radius, is_special, base_radius, is_dynamic, oscillation_phase]
striker_circles = []  # Format: [x, y]

# Utility Functions for GL_POINTS Drawing
def draw_point(x, y, color=(1.0, 1.0, 1.0), size=2):
    glColor3fv(color)
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw_midpoint_line(x1, y1, x2, y2, color=(1.0, 1.0, 1.0)):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    sx = 1 if x2 > x1 else -1
    sy = 1 if y2 > y1 else -1
    if dx > dy:
        err = dx / 2.0
        while x != x2:
            draw_point(int(x), int(y), color)
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y2:
            draw_point(int(x), int(y), color)
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    draw_point(int(x2), int(y2), color)

def draw_midpoint_circle(r, cx, cy, color=(1.0, 1.0, 1.0)):
    x, y = 0, r
    d = 1 - r
    def plot_circle_points(x, y):
        points = [
            (cx + x, cy + y), (cx - x, cy + y),
            (cx + x, cy - y), (cx - x, cy - y),
            (cx + y, cy + x), (cx - y, cy + x),
            (cx + y, cy - x), (cx - y, cy - x)
        ]
        for px, py in points:
            draw_point(int(px), int(py), color)
    plot_circle_points(x, y)
    while y > x:
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
        plot_circle_points(x, y)

def draw_spaceship(x, y):
    color = (1.0, 0.75, 0.0)
    draw_midpoint_line(x - 15, y, x + 15, y, color)
    draw_midpoint_line(x - 15, y, x, y + 30, color)
    draw_midpoint_line(x + 15, y, x, y + 30, color)

def draw_restart_button():
    x, y = restart_area
    color = (0.0, 0.5, 1.0)
    draw_midpoint_line(x + 10, y, x - 10, y, color)
    draw_midpoint_line(x - 10, y, x, y + 10, color)
    draw_midpoint_line(x - 10, y, x, y - 10, color)

def draw_pause_play_button():
    x, y = pause_play_area
    color = (1.0, 0.5, 0.0)
    if pause:
        draw_midpoint_line(x - 8, y - 10, x + 10, y, color)
        draw_midpoint_line(x - 8, y - 10, x - 8, y + 10, color)
        draw_midpoint_line(x - 8, y + 10, x + 10, y, color)
    else:
        draw_midpoint_line(x - 5, y - 10, x - 5, y + 10, color)
        draw_midpoint_line(x + 5, y - 10, x + 5, y + 10, color)

def draw_exit_button():
    x, y = cross_area
    color = (1.0, 0.0, 0.0)
    draw_midpoint_line(x - 10, y - 10, x + 10, y + 10, color)
    draw_midpoint_line(x - 10, y + 10, x + 10, y - 10, color)

def draw_buttons():
    draw_restart_button()
    draw_pause_play_button()
    draw_exit_button()

def generate_falling_circle():
    # Rule 1: Randomly generate a falling circle
    is_special = random.random() < 0.2
    is_dynamic = is_special and random.random() < 0.5
    base_radius = 15
    falling_circles.append([
        random.randint(base_radius, SCREEN_WIDTH - base_radius),
        random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - base_radius),
        base_radius,
        is_special,
        base_radius,
        is_dynamic,
        0.0
    ])

def draw_falling_circles():
    # Rule 2: Draw all falling circles
    for circle in falling_circles:
        if circle[3] and circle[5]:
            color = (0.0, 1.0, 0.0)
        elif circle[3]:
            color = (1.0, 0.0, 0.0)
        else:
            color = (1.0, 0.75, 0.0)
        draw_midpoint_circle(int(circle[2]), circle[0], circle[1], color)

def draw_projectiles():
    # Rule 3: Draw all projectiles
    for projectile in striker_circles:
        draw_midpoint_circle(r, projectile[0], projectile[1], (1.0, 1.0, 1.0))

def update_game():
    # Rule 4: Update the game, moving falling circles and projectiles
    global striker_circles, falling_circles, score, max_miss, misfire, game_over, last_frame_time
    current_time = time.time()
    delta_time = current_time - last_frame_time
    if not pause and not game_over:
        if len(falling_circles) < 3:
            generate_falling_circle()
        for circle in falling_circles[:]:
            circle[1] -= speed * 60 * delta_time
            if circle[5]:
                circle[6] += 0.2
                circle[2] = circle[4] + math.sin(circle[6]) * 5
            if circle[1] <= shooter_y + circle[2] and abs(circle[0] - shooter_x) <= circle[2]:
                game_over = True
                print_game_over()
                return
            if circle[1] < 0:
                falling_circles.remove(circle)
                max_miss -= 1
                if max_miss == 0:
                    game_over = True
                    print_game_over()
                    return
        for projectile in striker_circles[:]:
            projectile[1] += 300 * delta_time
            if projectile[1] > SCREEN_HEIGHT:
                striker_circles.remove(projectile)
                misfire += 1
                if misfire >= max_misfire:
                    game_over = True
                    print_game_over()
                    return
        for projectile in striker_circles[:]:
            for circle in falling_circles[:]:
                distance = math.sqrt((circle[0] - projectile[0]) ** 2 + (circle[1] - projectile[1]) ** 2)
                if distance < circle[2] + r:
                    if circle[3]:
                        score += 3 if circle[5] else 2
                    else:
                        score += 1
                    falling_circles.remove(circle)
                    striker_circles.remove(projectile)
                    break
    last_frame_time = current_time
    glutPostRedisplay()

def print_game_over():
    # Rule 5: Display "Game Over" and final score
    global falling_circles, game_over
    falling_circles.clear()
    print("Game Over! Final Score:", score)

def shoot():
    # Rule 6: Shoot a projectile
    if not game_over and not pause:
        striker_circles.append([shooter_x, shooter_y + 30])

def keyboard_input(key, x, y):
    # Rule 7: Handle keyboard input for moving the shooter and shooting
    global shooter_x
    if not game_over:
        if key == b"a" and shooter_x > 30:
            shooter_x -= 30
        elif key == b"d" and shooter_x < SCREEN_WIDTH - 30:
            shooter_x += 30
        elif key == b" ":
            shoot()

def mouse_input(button, state, x, y):
    # Rule 8: Handle mouse input for buttons (restart, pause, exit)
    global pause, game_over, score
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = SCREEN_HEIGHT - y
        if restart_area[0] - 20 <= x <= restart_area[0] + 20 and restart_area[1] - 20 <= y <= restart_area[1] + 20:
            restart_game()
        elif pause_play_area[0] - 20 <= x <= pause_play_area[0] + 20 and pause_play_area[1] - 20 <= y <= pause_play_area[1] + 20:
            pause = not pause
        elif cross_area[0] - 20 <= x <= cross_area[0] + 20 and cross_area[1] - 20 <= y <= cross_area[1] + 20:
            print("Goodbye! Final Score:", score)
            glutLeaveMainLoop()

def restart_game():
     # Rule 9: Restart the game
    global game_over, score, max_miss, misfire, falling_circles, striker_circles, pause
    game_over = False
    score = 0
    max_miss = 3
    misfire = 0
    falling_circles.clear()
    striker_circles.clear()
    pause = False
    print("Starting Over!")

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_spaceship(shooter_x, shooter_y)
    draw_falling_circles()
    draw_projectiles()
    draw_buttons()
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
    glutCreateWindow(b"Shoot the Circles!")
    gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard_input)
    glutMouseFunc(mouse_input)
    glutIdleFunc(update_game)
    glutMainLoop()

if __name__ == "__main__":
    main()
