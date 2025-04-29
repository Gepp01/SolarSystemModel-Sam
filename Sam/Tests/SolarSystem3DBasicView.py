import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# Planet colors for visualization
planet_colors = {
    'Mercury': '#8c8680',
    'Venus': '#e6c89c',
    'Earth': '#4f71be',
    'Mars': '#d1603d',
    'Jupiter': '#e0ae6f',
    'Saturn': '#c5ab6e',
    'Uranus': '#9fc4e7',
    'Neptune': '#4f71be',
    'Ceres': '#8c8680',
    'Pluto': '#ab9c8a',
    'Eris': '#d9d9d9',
    'Haumea': '#d9d9d9',
    'Makemake': '#c49e6c',
    'Sedna': '#bb5540'
}

# Orbital parameters for planets and dwarf planets
# Format: [semi_major_axis (km), eccentricity, inclination (deg), longitude_of_ascending_node (deg), 
#          argument_of_perihelion (deg), radius_scale_factor]
orbital_params = {
    'Mercury': [57.909e6, 0.2056, 7.005, 48.331, 29.124, 0.008],
    'Venus': [108.209e6, 0.0068, 3.39458, 76.680, 54.884, 0.02],
    'Earth': [149.598e6, 0.0167, 0.00005, -11.26064, 102.94719, 0.02],
    'Mars': [227.956e6, 0.0934, 1.850, 49.558, 286.502, 0.015],
    'Jupiter': [778.570e6, 0.0489, 1.303, 100.464, 273.867, 0.045],
    'Saturn': [1433.53e6, 0.0565, 2.485, 113.665, 339.392, 0.04],
    'Uranus': [2872.46e6, 0.0457, 0.773, 74.006, 96.998, 0.035],
    'Neptune': [4495.06e6, 0.0113, 1.77, 131.783, 273.187, 0.035],
    'Ceres': [414.01e6, 0.0758, 10.593, 80.393, 73.597, 0.005],
    'Pluto': [5906.38e6, 0.2488, 17.16, 110.299, 113.763, 0.01],
    'Eris': [10166e6, 0.44068, 44.04, 35.95, 151.639, 0.01],
    'Haumea': [6452e6, 0.19126, 28.19, 121.9, 239, 0.008],
    'Makemake': [6850e6, 0.159, 29, 79, 296, 0.008],
    'Sedna': [75600e6, 0.8459, 11.93, 144.31, 311.46, 0.006]
}

# Create a figure for 3D plotting
fig = plt.figure(figsize=(14, 12))
ax = fig.add_subplot(111, projection='3d')

# Calculate the focus distance (c) for the Sun's position
sun_x, sun_y, sun_z = 0, 0, 0  # Sun at origin for simplicity

# Create Sun (scaled for visibility)
sun_radius = orbital_params['Earth'][0] * 0.05  # Scale relative to Earth's orbit
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
sun_x_sphere = sun_radius * np.cos(u) * np.sin(v)
sun_y_sphere = sun_radius * np.sin(u) * np.sin(v)
sun_z_sphere = sun_radius * np.cos(v)
ax.plot_surface(sun_x_sphere, sun_y_sphere, sun_z_sphere, color='yellow', alpha=0.7)

# Plot orbits and planets
for i, (planet, params) in enumerate(orbital_params.items()):
    semi_major_axis, eccentricity, inclination, longitude_ascending_node, arg_perihelion, radius_factor = params
    
    # Convert angles from degrees to radians
    inclination = np.radians(inclination)
    longitude_ascending_node = np.radians(longitude_ascending_node)
    arg_perihelion = np.radians(arg_perihelion)
    
    # Calculate derived parameters
    semi_minor_axis = semi_major_axis * np.sqrt(1 - eccentricity**2)
    c = semi_major_axis * eccentricity  # Distance from center to focus
    
    # Generate points for the elliptical orbit
    theta = np.linspace(0, 2*np.pi, 1000)
    r = semi_major_axis * (1 - eccentricity**2) / (1 + eccentricity * np.cos(theta))
    
    # Basic orbit in x-y plane (before rotations)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = np.zeros_like(theta)
    
    # Apply argument of perihelion (rotation in the orbital plane)
    x_peri = x * np.cos(arg_perihelion) - y * np.sin(arg_perihelion)
    y_peri = x * np.sin(arg_perihelion) + y * np.cos(arg_perihelion)
    z_peri = z
    
    # Apply the orbital inclination (rotation around x-axis)
    x_inclined = x_peri
    y_inclined = y_peri * np.cos(inclination) - z_peri * np.sin(inclination)
    z_inclined = y_peri * np.sin(inclination) + z_peri * np.cos(inclination)
    
    # Apply rotation for longitude of ascending node (rotation around z-axis)
    x_rotated = x_inclined * np.cos(longitude_ascending_node) - y_inclined * np.sin(longitude_ascending_node)
    y_rotated = x_inclined * np.sin(longitude_ascending_node) + y_inclined * np.cos(longitude_ascending_node)
    z_rotated = z_inclined
    
    # Plot orbit
    ax.plot(x_rotated, y_rotated, z_rotated, color=planet_colors[planet], linewidth=1.5, alpha=0.7, label=f'{planet} Orbit')
    
    # Calculate current position (arbitrary point on orbit for visualization)
    # Different starting positions for each planet to avoid overlap
    planet_theta = (i * 30) % 360  # Use the loop index instead of dict.keys().index()
    planet_theta = np.radians(planet_theta)
    
    planet_r = semi_major_axis * (1 - eccentricity**2) / (1 + eccentricity * np.cos(planet_theta))
    planet_x = planet_r * np.cos(planet_theta)
    planet_y = planet_r * np.sin(planet_theta)
    planet_z = 0
    
    # Apply the same rotations as for the orbit
    planet_x_peri = planet_x * np.cos(arg_perihelion) - planet_y * np.sin(arg_perihelion)
    planet_y_peri = planet_x * np.sin(arg_perihelion) + planet_y * np.cos(arg_perihelion)
    planet_z_peri = planet_z
    
    planet_x_inclined = planet_x_peri
    planet_y_inclined = planet_y_peri * np.cos(inclination) - planet_z_peri * np.sin(inclination)
    planet_z_inclined = planet_y_peri * np.sin(inclination) + planet_z_peri * np.cos(inclination)
    
    planet_x_rotated = planet_x_inclined * np.cos(longitude_ascending_node) - planet_y_inclined * np.sin(longitude_ascending_node)
    planet_y_rotated = planet_x_inclined * np.sin(longitude_ascending_node) + planet_y_inclined * np.cos(longitude_ascending_node)
    planet_z_rotated = planet_z_inclined
    
    # Create planet (scaled for visibility)
    planet_radius = orbital_params['Earth'][0] * radius_factor
    ax.scatter([planet_x_rotated], [planet_y_rotated], [planet_z_rotated], 
               color=planet_colors[planet], s=planet_radius*0.2, label=planet)

# Add reference grid and axes
ax.set_xlabel('X (km)')
ax.set_ylabel('Y (km)')
ax.set_zlabel('Z (km)')
ax.set_title("Solar System with Planets and Dwarf Planets (Not to Scale)", fontsize=16)

# Use scientific notation for axis labels
ax.ticklabel_format(style='sci', axis='both', scilimits=(0,0))

# Create a custom legend with fewer entries for clarity
inner_planets = plt.Line2D([0], [0], color='black', linewidth=0, marker='o', 
                          markersize=8, markerfacecolor=planet_colors['Mercury'], label='Inner Planets')
outer_planets = plt.Line2D([0], [0], color='black', linewidth=0, marker='o', 
                          markersize=8, markerfacecolor=planet_colors['Jupiter'], label='Outer Planets')
dwarf_planets = plt.Line2D([0], [0], color='black', linewidth=0, marker='o', 
                          markersize=8, markerfacecolor=planet_colors['Pluto'], label='Dwarf Planets')
sun = plt.Line2D([0], [0], color='black', linewidth=0, marker='o', 
                markersize=12, markerfacecolor='yellow', label='Sun')

legend1 = ax.legend(handles=[sun, inner_planets, outer_planets, dwarf_planets], 
                   loc='upper left', bbox_to_anchor=(1.05, 1), title='Legend')
ax.add_artist(legend1)

# Create secondary legend for individual planets
legend_elements = []
for planet, color in planet_colors.items():
    legend_elements.append(plt.Line2D([0], [0], color=color, lw=2, label=planet))
    
legend2 = ax.legend(handles=legend_elements, loc='upper left', 
                   bbox_to_anchor=(1.05, 0.6), title='Planets')

# Ensure the 3D plot has equal scale
max_range = max([
    np.max([np.abs(orbital_params['Mercury'][0]), np.abs(orbital_params['Neptune'][0])]),
    np.max([np.abs(orbital_params['Mercury'][0]), np.abs(orbital_params['Neptune'][0])]),
    np.max([np.abs(orbital_params['Mercury'][0]), np.abs(orbital_params['Neptune'][0])])
]) * 1.2

ax.set_xlim(-max_range, max_range)
ax.set_ylim(-max_range, max_range)
ax.set_zlim(-max_range, max_range)

plt.tight_layout()
plt.subplots_adjust(right=0.8)  # Make room for the legend on the right
plt.show()

# Animation function for 3D solar system
def animate_solar_system():
    from matplotlib.animation import FuncAnimation
    
    # Create a new figure for animation
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Draw the Sun
    ax.plot_surface(sun_x_sphere, sun_y_sphere, sun_z_sphere, color='yellow', alpha=0.7)
    
    # Initialize planet markers
    planet_points = {}
    
    # Plot orbits and initialize planet points
    for planet, params in orbital_params.items():
        semi_major_axis, eccentricity, inclination, longitude_ascending_node, arg_perihelion, radius_factor = params
        
        # Convert angles from degrees to radians
        inclination = np.radians(inclination)
        longitude_ascending_node = np.radians(longitude_ascending_node)
        arg_perihelion = np.radians(arg_perihelion)
        
        # Calculate derived parameters
        semi_minor_axis = semi_major_axis * np.sqrt(1 - eccentricity**2)
        
        # Generate points for the elliptical orbit
        theta = np.linspace(0, 2*np.pi, 1000)
        r = semi_major_axis * (1 - eccentricity**2) / (1 + eccentricity * np.cos(theta))
        
        # Basic orbit in x-y plane (before rotations)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = np.zeros_like(theta)
        
        # Apply argument of perihelion (rotation in the orbital plane)
        x_peri = x * np.cos(arg_perihelion) - y * np.sin(arg_perihelion)
        y_peri = x * np.sin(arg_perihelion) + y * np.cos(arg_perihelion)
        z_peri = z
        
        # Apply the orbital inclination (rotation around x-axis)
        x_inclined = x_peri
        y_inclined = y_peri * np.cos(inclination) - z_peri * np.sin(inclination)
        z_inclined = y_peri * np.sin(inclination) + z_peri * np.cos(inclination)
        
        # Apply rotation for longitude of ascending node (rotation around z-axis)
        x_rotated = x_inclined * np.cos(longitude_ascending_node) - y_inclined * np.sin(longitude_ascending_node)
        y_rotated = x_inclined * np.sin(longitude_ascending_node) + y_inclined * np.cos(longitude_ascending_node)
        z_rotated = z_inclined
        
        # Plot orbit
        ax.plot(x_rotated, y_rotated, z_rotated, color=planet_colors[planet], linewidth=1, alpha=0.5)
        
        # Initialize planet marker (we'll update its position in the animation)
        planet_point, = ax.plot([x_rotated[0]], [y_rotated[0]], [z_rotated[0]], 
                              'o', color=planet_colors[planet], markersize=radius_factor*150)
        
        # Store orbit data and point object for animation updates
        planet_points[planet] = {
            'point': planet_point,
            'x': x_rotated,
            'y': y_rotated,
            'z': z_rotated
        }
    
    # Set axis limits
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    ax.set_zlim(-max_range, max_range)
    
    # Title and labels
    ax.set_title("Solar System Animation", fontsize=14)
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')
    
    # Use scientific notation for axis labels
    ax.ticklabel_format(style='sci', axis='both', scilimits=(0,0))
    
    # Create secondary legend for individual planets
    legend_elements = []
    for planet, color in planet_colors.items():
        legend_elements.append(plt.Line2D([0], [0], color=color, marker='o', 
                                         linestyle='', markersize=5, label=planet))
        
    legend = ax.legend(handles=legend_elements, loc='upper left', 
                      bbox_to_anchor=(1.05, 1), title='Planets')
    
    # Function to update planet positions
    def update(frame):
        # Different speeds for different planets (realistic orbital periods)
        for planet, params in orbital_params.items():
            # Adjust animation speed based on orbital parameters
            # Inner planets move faster than outer planets
            semi_major_axis = params[0]
            speed_factor = np.sqrt(orbital_params['Earth'][0] / semi_major_axis) * 2
            
            # Calculate index based on speed (faster for inner planets)
            idx = int((frame * speed_factor) % 1000)
            
            # Update position
            planet_data = planet_points[planet]
            planet_data['point'].set_data([planet_data['x'][idx]], [planet_data['y'][idx]])
            planet_data['point'].set_3d_properties([planet_data['z'][idx]])
        
        # Return all planets for animation update
        return [data['point'] for data in planet_points.values()]
    
    # Create animation
    ani = FuncAnimation(fig, update, frames=500, interval=50, blit=True)
    
    plt.tight_layout()
    plt.subplots_adjust(right=0.8)  # Make room for the legend
    
    return ani

# Uncomment to run the animation
ani = animate_solar_system()
from IPython.display import HTML
HTML(ani.to_jshtml())