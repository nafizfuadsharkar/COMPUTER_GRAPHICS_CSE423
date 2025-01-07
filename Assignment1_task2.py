from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


points = []  # Stores points as tuples of (x, y, color, direction_x, direction_y)
box_left = 0  # Left boundary of the box
box_right = 400  # Right boundary of the box
box_bottom = 0  # Bottom boundary of the box
box_top = 300  # Top boundary of the box
point_size = 10  # Size of each point
point_speed = 0.075  # Speed of point movement

# Variables to track the left mouse button state and transition start time
left_button_clicked = False  # Toggles blinking functionality
transition_start_time = 0  # Start time for blinking transitions

# Variable to track whether the Space bar is pressed
space_bar_pressed = False  # Freezes and unfreezes the simulation

# Variable to store the original point colors
original_colors = []  # Keeps track of original colors for blinking

def render_points():
    """
    Draw and update all points on the screen, considering current states like blinking or freezing.
    """
    global left_button_clicked, transition_start_time, space_bar_pressed

    glEnable(GL_POINT_SMOOTH)  # Enable smooth rendering for points
    glPointSize(point_size)  # Set the size of the points
    glBegin(GL_POINTS)

    for i in range(len(points)):
        x, y, color, direction_x, direction_y = points[i]

        # If Space bar is pressed, freeze all points
        if space_bar_pressed:
            direction_x = 0
            direction_y = 0
            left_button_clicked = False  # Disable blinking during freezing

        # Handle blinking functionality when the left mouse button is clicked
        if left_button_clicked and not space_bar_pressed:
            current_time = glutGet(GLUT_ELAPSED_TIME)
            time_diff = (current_time - transition_start_time) % 800  # Blinking cycle of 800ms

            if time_diff < 100:  # Blink to background color (black) for 100ms
                color = (0.0, 0.0, 0.0)
            else:  # Restore original color
                color = original_colors[i]

        glColor3f(*color)  # Set the point color
        glVertex2f(x, y)  # Draw the point

        # Update the position of the point
        x += point_speed * direction_x
        y += point_speed * direction_y

        # Reflect the point when it hits the boundaries of the box
        if x < box_left + point_size:
            x = box_left + point_size
            direction_x = -direction_x
        elif x > box_right - point_size:
            x = box_right - point_size
            direction_x = -direction_x
        if y < box_bottom + point_size:
            y = box_bottom + point_size
            direction_y = -direction_y
        elif y > box_top - point_size:
            y = box_top - point_size
            direction_y = -direction_y

        # Update the point data
        points[i] = (x, y, color, direction_x, direction_y)

    glEnd()

def spawn_point(x, y):
    """
    Create a new random point at the given coordinates within the box.
    """
    if box_left < x < box_right and box_bottom < y < box_top:
        # Generate a random color
        color = (random.random(), random.random(), random.random())

        # Assign a random diagonal direction
        direction_x = random.choice([-1, 1])
        direction_y = random.choice([-1, 1])

        # Add the new point to the list
        points.append((x, y, color, direction_x, direction_y))
        original_colors.append(color)  # Save the color for blinking

def handle_mouse_click(button, state, x, y):
    """
    Handle mouse click events for spawning points or toggling blinking.
    """
    global left_button_clicked, transition_start_time, space_bar_pressed

    if space_bar_pressed:
        return  # Ignore mouse clicks when frozen

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        # Convert screen coordinates to OpenGL coordinates and spawn a point
        spawn_point(x / 2, box_top - y / 2)
        print("New point added")
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Toggle blinking functionality
        left_button_clicked = not left_button_clicked
        if left_button_clicked:
            transition_start_time = glutGet(GLUT_ELAPSED_TIME)  # Record the start time
            print("Blinking Function Turned On")
        else:
            print("Blinking Function Turned Off")

def handle_arrow_keys(key, x, y):
    """
    Handle up and down arrow keys to adjust point speed.
    """
    global point_speed

    if key == GLUT_KEY_UP:
        point_speed += 0.0025  # Increase speed
        print("Speed Increased")
    elif key == GLUT_KEY_DOWN:
        if point_speed <= 0:
            point_speed = 0
            print("Speed limit reached")
        else:
            point_speed -= 0.0025  # Decrease speed
            print("Speed Decreased")

def handle_spacebar(key, x, y):
    """
    Handle Space bar press to freeze/unfreeze the simulation.
    """
    global space_bar_pressed, left_button_clicked

    if key == b' ':  # Space bar toggles freezing state
        space_bar_pressed = not space_bar_pressed
        if space_bar_pressed:
            left_button_clicked = False  # Disable blinking during freezing
            # Stop all points
            for i in range(len(points)):
                x, y, color, direction_x, direction_y = points[i]
                points[i] = (x, y, color, 0, 0)
            print("Points Frozen")
        else:
            # Resume all points with random directions
            for i in range(len(points)):
                direction_x = random.choice([-1, 1])
                direction_y = random.choice([-1, 1])
                points[i] = (points[i][0], points[i][1], points[i][2], direction_x, direction_y)
            print("Points Unfrozen")

def render_box():
    """
    Draw the boundary box.
    """
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(box_right, box_top)
    glVertex2f(box_left, box_top)

    glVertex2f(box_left, box_top)
    glVertex2f(box_left, box_bottom)

    glVertex2f(box_right, box_bottom)
    glVertex2f(box_left, box_bottom)

    glVertex2f(box_right, box_bottom)
    glVertex2f(box_right, box_top)
    glEnd()

def setup_viewport():
    """
    Set up the 2D orthographic projection for rendering.
    """
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 400, 0, 300, -1, 1)  
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def render_scene():
    """
    Render the entire scene including the box and points.
    """
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    setup_viewport()

    glColor3f(1.0, 1.0, 1.0)  # Set color for the box

    render_box()  # Draw the boundary
    render_points()  # Draw and update points

    glutSwapBuffers()

def main():
    """
    Entry point for the application.
    """
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(400, 300)  
    glutCreateWindow(b"The Amazing Box")
    glutDisplayFunc(render_scene)
    glutMouseFunc(handle_mouse_click)
    glutSpecialFunc(handle_arrow_keys)
    glutKeyboardFunc(handle_spacebar)
    glutIdleFunc(render_scene)
    glutMainLoop()

if __name__ == "__main__":
    main()
