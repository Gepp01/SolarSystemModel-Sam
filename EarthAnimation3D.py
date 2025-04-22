import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# Earth orbital parameters (J2000)
semi_major_axis = 149.598e6  # km
eccentricity = 0.0167
inclination = np.radians(0.00005)  # Convert from degrees to radians
longitude_ascending_node = np.radians(-11.26064)  # Convert from degrees to radians
longitude_perihelion = np.radians(102.94719)  # Convert from degrees to radians

# Calculate the semi-minor axis
semi_minor_axis = semi_major_axis * np.sqrt(1 - eccentricity**2)  # km

# Calculate the distance from center to focus
c = semi_major_axis * eccentricity  # km

# Calculate perihelion and aphelion
perihelion = semi_major_axis * (1 - eccentricity)  # km
aphelion = semi_major_axis * (1 + eccentricity)  # km

# Create a figure for 3D plotting
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Generate points for the elliptical orbit
theta = np.linspace(0, 2*np.pi, 1000)
r = semi_major_axis * (1 - eccentricity**2) / (1 + eccentricity * np.cos(theta))

# Basic orbit in x-y plane (before applying inclination and rotations)
x = r * np.cos(theta)
y = r * np.sin(theta)
z = np.zeros_like(theta)

# Apply the orbital inclination (rotation around x-axis)
x_inclined = x
y_inclined = y * np.cos(inclination) - z * np.sin(inclination)
z_inclined = y * np.sin(inclination) + z * np.cos(inclination)

# Apply rotation for longitude of ascending node (rotation around z-axis)
x_rotated = x_inclined * np.cos(longitude_ascending_node) - y_inclined * np.sin(longitude_ascending_node)
y_rotated = x_inclined * np.sin(longitude_ascending_node) + y_inclined * np.cos(longitude_ascending_node)
z_rotated = z_inclined

# Plot orbit
ax.plot(x_rotated, y_rotated, z_rotated, color='blue', linewidth=2, label='Earth Orbit')

# Plot the Sun at the focus
# We need to offset the sun from (0,0,0) by the focus distance
sun_x = -c * np.cos(longitude_ascending_node)
sun_y = -c * np.sin(longitude_ascending_node)
sun_z = 0

# Create Sun (scaled for visibility)
sun_radius = semi_major_axis * 0.05
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
sun_x_sphere = sun_x + sun_radius * np.cos(u) * np.sin(v)
sun_y_sphere = sun_y + sun_radius * np.sin(u) * np.sin(v)
sun_z_sphere = sun_z + sun_radius * np.cos(v)
ax.plot_surface(sun_x_sphere, sun_y_sphere, sun_z_sphere, color='yellow', alpha=0.7, label='Sun')

# Calculate Earth's position at perihelion
earth_theta = 0  # perihelion occurs at theta = 0
earth_r = semi_major_axis * (1 - eccentricity**2) / (1 + eccentricity * np.cos(earth_theta))
earth_x = earth_r * np.cos(earth_theta)
earth_y = earth_r * np.sin(earth_theta)
earth_z = 0

# Apply inclination and rotation to Earth's position
earth_x_inclined = earth_x
earth_y_inclined = earth_y * np.cos(inclination) - earth_z * np.sin(inclination)
earth_z_inclined = earth_y * np.sin(inclination) + earth_z * np.cos(inclination)

earth_x_rotated = earth_x_inclined * np.cos(longitude_ascending_node) - earth_y_inclined * np.sin(longitude_ascending_node)
earth_y_rotated = earth_x_inclined * np.sin(longitude_ascending_node) + earth_y_inclined * np.cos(longitude_ascending_node)
earth_z_rotated = earth_z_inclined

# Create Earth (scaled for visibility)
earth_radius = semi_major_axis * 0.03
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
earth_x_sphere = earth_x_rotated + earth_radius * np.cos(u) * np.sin(v)
earth_y_sphere = earth_y_rotated + earth_radius * np.sin(u) * np.sin(v)
earth_z_sphere = earth_z_rotated + earth_radius * np.cos(v)
ax.plot_surface(earth_x_sphere, earth_y_sphere, earth_z_sphere, color='blue', alpha=0.7)

# Mark perihelion and aphelion
perihelion_x = (perihelion - c) * np.cos(longitude_ascending_node)
perihelion_y = (perihelion - c) * np.sin(longitude_ascending_node)
perihelion_z = 0
ax.scatter([perihelion_x], [perihelion_y], [perihelion_z], color='red', s=100, label='Perihelion')

aphelion_x = -(aphelion - c) * np.cos(longitude_ascending_node)
aphelion_y = -(aphelion - c) * np.sin(longitude_ascending_node)
aphelion_z = 0
ax.scatter([aphelion_x], [aphelion_y], [aphelion_z], color='green', s=100, label='Aphelion')

# Add reference grid and axes
ax.set_xlabel('X (km)')
ax.set_ylabel('Y (km)')
ax.set_zlabel('Z (km)')
ax.set_title("Earth's 3D Orbit Around the Sun (Not to Scale)", fontsize=14)

# Use scientific notation for axis labels
ax.ticklabel_format(style='sci', axis='both', scilimits=(0,0))

# Ensure the 3D plot has equal scale
max_range = np.array([x_rotated.max()-x_rotated.min(), 
                      y_rotated.max()-y_rotated.min(), 
                      z_rotated.max()-z_rotated.min()]).max() / 2.0
mid_x = (x_rotated.max()+x_rotated.min()) / 2
mid_y = (y_rotated.max()+y_rotated.min()) / 2
mid_z = (z_rotated.max()+z_rotated.min()) / 2
ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)

ax.legend()
plt.tight_layout()
plt.show()

# Animation function for 3D orbit
def animate_3d_orbit():
    from matplotlib.animation import FuncAnimation
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.animation as animation
    
    # Create a new figure for animation
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Draw the orbit
    ax.plot(x_rotated, y_rotated, z_rotated, color='blue', linewidth=2)
    
    # Draw the Sun
    ax.plot_surface(sun_x_sphere, sun_y_sphere, sun_z_sphere, color='yellow', alpha=0.7)
    
    # Initialize Earth as a scatter point for simplicity in animation
    earth_point, = ax.plot([earth_x_rotated], [earth_y_rotated], [earth_z_rotated], 
                         'bo', markersize=10, label='Earth')
    
    # Set axis limits
    max_range = np.array([x_rotated.max()-x_rotated.min(), 
                          y_rotated.max()-y_rotated.min(), 
                          z_rotated.max()-z_rotated.min()]).max() / 2.0
    mid_x = (x_rotated.max()+x_rotated.min()) / 2
    mid_y = (y_rotated.max()+y_rotated.min()) / 2
    mid_z = (z_rotated.max()+z_rotated.min()) / 2
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)
    
    # Title and labels
    ax.set_title("Earth's 3D Orbit Animation", fontsize=14)
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')
    
    # Function to update Earth position
    def update(frame):
        idx = int(frame * len(x_rotated) / 100) % len(x_rotated)
        earth_point.set_data([x_rotated[idx]], [y_rotated[idx]])
        earth_point.set_3d_properties([z_rotated[idx]])
        return earth_point,
    
    # Create animation
    ani = FuncAnimation(fig, update, frames=100, interval=100, blit=False)
    
    return ani

# Uncomment to run the animation
ani = animate_3d_orbit()
from IPython.display import HTML
HTML(ani.to_jshtml())