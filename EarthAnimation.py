import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.patches import Ellipse

# Earth orbital parameters (J2000)
semi_major_axis = 149.598e6  # km
eccentricity = 0.0167
perihelion = semi_major_axis * (1 - eccentricity)  # km
aphelion = semi_major_axis * (1 + eccentricity)  # km

# Calculate the semi-minor axis
semi_minor_axis = semi_major_axis * np.sqrt(1 - eccentricity**2)  # km

# Calculate the distance from center to focus
c = semi_major_axis * eccentricity  # km

# Create a figure and axis with equal aspect ratio
plt.figure(figsize=(10, 8))
ax = plt.gca()

# Set aspect ratio to equal to ensure circle looks like a circle
ax.set_aspect('equal')

# Draw the orbit (ellipse centered at origin)
orbit = Ellipse((0, 0), 2*semi_major_axis, 2*semi_minor_axis, 
                fill=False, edgecolor='blue', linewidth=1.5)
ax.add_patch(orbit)

# Draw the Sun at one focus of the ellipse (-c, 0)
sun_radius = 696340  # km (actual radius of Sun)
# Use a scaled radius for better visibility
display_sun_radius = semi_major_axis * 0.05
sun = Circle((-c, 0), display_sun_radius, fill=True, color='yellow', zorder=2, 
             label=f"Sun (radius scaled for visibility)")

# Calculate Earth's position at a specific point (let's use perihelion)
earth_x = perihelion - c
earth_y = 0

# Draw Earth (scaled for visibility)
earth_radius = 6371.0  # km (actual radius)
# Use a scaled radius for better visibility
display_earth_radius = semi_major_axis * 0.03
earth = Circle((earth_x, earth_y), display_earth_radius, fill=True, color='blue', zorder=2,
               label=f"Earth (radius scaled for visibility)")

# Add the Sun and Earth to the plot
ax.add_patch(sun)
ax.add_patch(earth)

# Add perihelion and aphelion markers
plt.scatter([perihelion - c], [0], color='red', s=50, zorder=3, label='Perihelion')
plt.scatter([-(aphelion - c)], [0], color='green', s=50, zorder=3, label='Aphelion')

# Add text labels for distances
plt.text(perihelion - c, display_earth_radius*2, f'Perihelion\n{perihelion/1e6:.1f} million km', 
         ha='center', va='bottom')
plt.text(-(aphelion - c), display_earth_radius*2, f'Aphelion\n{aphelion/1e6:.1f} million km', 
         ha='center', va='bottom')

# Add legend, title, and grid
plt.legend(loc='upper right')
plt.title("Earth's Orbit Around the Sun (Not to Scale)", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)

# Use scientific notation for axis labels
plt.ticklabel_format(style='sci', axis='both', scilimits=(0,0))
plt.xlabel('X (km)')
plt.ylabel('Y (km)')

# Add annotations
plt.figtext(0.5, 0.01, 
            f"Semi-major axis: {semi_major_axis/1e6:.1f} million km\n"
            f"Eccentricity: {eccentricity}\n"
            f"Note: Sun and Earth sizes are not to scale", 
            ha='center', fontsize=10)

plt.tight_layout()
plt.show()

# If you want to animate the orbit over time:
def animate_orbit():
    from matplotlib.animation import FuncAnimation
    
    # Create a new figure for animation
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_aspect('equal')
    
    # Draw the orbit
    orbit = Ellipse((0, 0), 2*semi_major_axis, 2*semi_minor_axis, 
                    fill=False, edgecolor='blue', linewidth=1.5)
    ax.add_patch(orbit)
    
    # Draw the Sun
    sun = Circle((-c, 0), display_sun_radius, fill=True, color='yellow')
    ax.add_patch(sun)
    
    # Initialize Earth
    earth = Circle((0, 0), display_earth_radius, fill=True, color='blue')
    ax.add_patch(earth)
    
    # Set axis limits
    limit = semi_major_axis * 1.1
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    
    # Title and grid
    ax.set_title("Earth's Orbit Animation", fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Function to update Earth position
    def update(frame):
        # Calculate Earth position from true anomaly
        true_anomaly = np.radians(frame)
        radius = semi_major_axis * (1 - eccentricity**2) / (1 + eccentricity * np.cos(true_anomaly))
        x = radius * np.cos(true_anomaly) - c
        y = radius * np.sin(true_anomaly)
        
        # Update Earth position
        earth.set_center((x, y))
        return earth,
    
    # Create animation
    animation = FuncAnimation(fig, update, frames=np.linspace(0, 360, 180),
                              interval=50, blit=True)
    
    plt.tight_layout()
    return animation

# Uncomment the following lines to run the animation
anim = animate_orbit()
from IPython.display import HTML
HTML(anim.to_jshtml())