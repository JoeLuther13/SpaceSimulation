from vpython import *

# Allow an increase in the size of the display
canvas(width=1000, height=600, resizeable=True, align="right", texture="Texture/2k_stars_milky_way.jpg")
scene.title = "Solar System Comet Simulation"

# Define fps with an adjustable timescale
fps = 60
timescale = 2000000

# Create default planets, altering real radii as needed for visibility
sun = sphere(texture="Textures/2k_sun.jpg", emissive = True, radius=11E9, mass=1.9885E30)
mercury = sphere(vel=vec(0,47.87E3,0), pos=vec(48E9,0,0), texture="Textures/2k_mercury.jpg", emissive=False, radius=4E9, mass=3.3011E23)
venus = sphere(vel=vec(0,35.02E3,0), pos=vec(108.939E9,0,0), texture="Textures/2k_venus_atmosphere.jpg", emissive = False, radius=5E9, mass=4.8673E24)
earth = sphere(vel=vec(0,29.79E3,0), pos=vec(149.6E9,0,0), texture="Textures/2k_earth_daymap.jpg", emissive=False, radius=6E9, mass=5.9722E24)
mars = sphere(vel=vec(0,24.077E3,0), pos=vec(228E9,0,0), texture="Textures/2k_mars.jpg", emissive=False, radius=5E9, mass=6.4169E23)
jupiter = sphere(vel=vec(0,13.07E3,0), pos=vec(778E9,0,0), texture="Textures/2k_jupiter.jpg", emissive=False, radius=9E9, mass=1.8982E27)
# saturn = sphere(vel=vec(0,9.69E3,0), pos=vec(-1400E9,0,0), color=color.yellow, emissive=False, radius=8E9, mass=5.6834E26)
# uranus = sphere(vel=vec(0,6.81E3,0), pos=vec(-1800E9,0,0), color=color.blue, emissive=False, radius=7E9, mass=8.6810E25)
# neptune = sphere(vel=vec(0,5.43E3,0), pos=vec(-2800E9,0,0), color=color.blue, emissive=False, radius=7E9, mass=1.02E26)
planets = [mercury, venus, earth, mars, jupiter]#, saturn, uranus, neptune] These planets were removed because the extra zoom hurt the visability
comets = []

# Create indicater for where comets will spawn
spawn_marker = cone(pos=vec(-1000E9,0,0), color=color.white, emissive=True, radius=1E10, length=3E10)

# Function for changing y position of marker
def set_comet_y(slider):
    spawn_marker.pos.y = slider.value
    y_pos_label.text = str(slider.value) + "m\n"

# Function to spawn a comet
def spawn_comet():
    comet = sphere(vel=vec(25E3,0,0), pos=spawn_marker.pos, texture="Textures/comet.jpg", emissive=True, radius=4E9, mass=2E12, make_trail=True)
    comets.append(comet)

# Create widgets to change values
y_pos_slider = slider(min=-500E9, max=500E9, value=0, bind=set_comet_y, vertical=True, align="left")
y_pos_label = wtext(text=str(y_pos_slider.value) + "m\n")
spawn_button = button(bind=spawn_comet, text="Spawn Comet")

# Function to calculate force of gravity given two objects
def calculate_gravity(s1, s2):
    G = 6.67E-11
    return G * s1.mass * s2.mass * hat(s2.pos - s1.pos) / (mag(s2.pos - s1.pos))**2 

# Function to update position of object
def position_update(s):
    s.pos += s.vel * dt

# Function to update velocity of an object
def velocity_update(s, F):
    s.vel += (F / s.mass) * dt

# Keep the program running while open
while True:
    dt = (1/fps) * timescale 
    rate(fps)
    # Calculate position and velocity for each planet
    for p in planets:
        velocity_update(p, calculate_gravity(p, sun))
        position_update(p)
    # Calculate gravity on comet and update position
    for count, comet in enumerate(comets):
        comet_net_force = calculate_gravity(comet, sun)
        for p in planets:
            comet_net_force += calculate_gravity(comet, p)
        for other_count, c in enumerate(comets):
            if other_count == count:
                pass
            else:
                comet_net_force += calculate_gravity(comet, c)
        velocity_update(comet, comet_net_force)
        position_update(comet)