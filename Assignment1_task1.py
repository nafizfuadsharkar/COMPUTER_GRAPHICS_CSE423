from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


rain_enabled = False  # Controls whether rain is falling
rain_x = 200  # Starting x-coordinate for rain
rain_y = 425  # Starting y-coordinate for rain
rain_bend = 0  # Controls the horizontal bending of rain
background_color = [1.0, 1.0, 1.0]  # Default background color (day mode)
raindrop_color = [0.0, 0.0, 0.0]  # Default raindrop color (black)

# Function to draw a single point at (x, y)
def draw_raindrop(x, y):
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

# Function to create animated raindrops at random positions
def draw_rain_animation():
    glPointSize(4)
    glBegin(GL_POINTS)
    for _ in range(50):  # Generate 50 random raindrop points
        x = random.randint(1, 500)  # Random x-coordinate
        y = random.randint(1, 500)  # Random y-coordinate
        glColor3f(*raindrop_color)  # Use current raindrop color
        glVertex2f(x, y)
    glEnd()

# Function to draw the house using lines (walls, door, and windows)
def draw_house():
    glLineWidth(3.22)
    glBegin(GL_LINES)

    # House outer walls
    glColor3f(1.0, 0.0, 1.0)  # Purple color for walls
    glVertex2f(50, 100)  
    glVertex2f(250, 100)  

    glVertex2f(50, 100)  
    glVertex2f(50, 250)  

    glVertex2f(250, 100)  
    glVertex2f(250, 250)  

    glVertex2f(50, 250)  
    glVertex2f(250, 250)  

    # Door
    glColor3f(1.0, 1.0, 0.0)  # Yellow color for door
    glVertex2f(100, 100)  
    glVertex2f(100, 150)  

    glVertex2f(100, 100)  
    glVertex2f(150, 100)  

    glVertex2f(150, 100)  
    glVertex2f(150, 150)  

    glVertex2f(100, 150)  
    glVertex2f(150, 150)  

    # Window
    glColor3f(0.0, 1.0, 1.0)  # Cyan color for window
    glVertex2f(160, 190)  
    glVertex2f(200, 190)  

    glVertex2f(160, 190)  
    glVertex2f(160, 220)  

    glVertex2f(200, 190)  
    glVertex2f(200, 220)  

    glVertex2f(160, 220)  
    glVertex2f(200, 220)  

    glEnd()

# Function to draw the triangular roof of the house
def draw_roof():
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)  # Red color for roof
    glVertex2f(50, 250)  
    glVertex2f(250, 250)  
    glVertex2f(145, 385)  
    glEnd()

# Function to set the background color
def set_background():
    glClearColor(*background_color, 1.0)  # Use current background color
    glClear(GL_COLOR_BUFFER_BIT)

# Function to configure the viewing area
def configure_viewport():
    glViewport(0, 0, 500, 450)  # Set the drawing area
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 450, 0.0, 1.0)  # 2D orthogonal projection
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# Mouse handler to toggle rain on/off
def handle_mouse_input(button, state, x, y):
    global rain_enabled
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        rain_enabled = not rain_enabled  # Toggle rain
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        rain_enabled = False  # Stop rain

# Special key handler to bend rain left/right
def handle_arrow_keys(key, x, y):
    global rain_bend
    if key == GLUT_KEY_LEFT:
        rain_bend -= 1  # Bend rain left
        print("Rain bent towards left")
    elif key == GLUT_KEY_RIGHT:
        rain_bend += 1  # Bend rain right
        print("Rain bent towards right")

# Keyboard handler to switch day/night modes
def handle_keyboard_input(key, x, y):
    global background_color, raindrop_color
    if key == b'd':
        # Switch to day mode
        background_color = [1.0, 1.0, 1.0]  # White background
        raindrop_color = [0.0, 0.0, 0.0]  # Black raindrop
        print("Switched to Day Mode")
    elif key == b'n':
        # Switch to night mode
        background_color = [0.0, 0.0, 0.0]  # Black background
        raindrop_color = [1.0, 1.0, 1.0]  # White raindrop
        print("Switched to Night Mode")

# Main display function
def render_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear screen
    glLoadIdentity()
    configure_viewport()

    set_background()  # Set background color
    draw_house()  # Draw the house
    draw_raindrop(145, 120)  # Static raindrop (example point)

    if rain_enabled:
        draw_rain_animation()  # Draw falling rain if enabled

    draw_roof()  # Draw the house roof
    glutSwapBuffers()  # Swap buffers for double buffering

# Timer function to update the scene periodically
def rain_animation_timer(value):
    glutTimerFunc(100, rain_animation_timer, 0)  # Re-trigger the timer
    glutPostRedisplay()  # Request a redraw of the screen

# Initialize the OpenGL environment and start the main loop
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)  # Window dimensions
glutInitWindowPosition(125, 0)  # Window position on screen
window = glutCreateWindow(b"Interactive Rainfall Simulation")
glutDisplayFunc(render_scene)
glutMouseFunc(handle_mouse_input)
glutSpecialFunc(handle_arrow_keys)
glutKeyboardFunc(handle_keyboard_input)
glutTimerFunc(100, rain_animation_timer, 0)  # Start animation timer
glutMainLoop()
