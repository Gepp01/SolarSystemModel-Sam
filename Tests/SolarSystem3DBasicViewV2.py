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
# Format: [semi_major_axis (AU), eccentricity, inclination (deg), longitude_of_ascending_node (deg), 
#          argument_of_perihelion (deg), radius_scale_factor]
# Using Astronomical Units (AU) for better scaling
orbital_params = {
    'Mercury': [0.387, 0.2056, 7.005, 48.331, 29.124, 0.008],
    'Venus': [0.723, 0.0068, 3.39458, 76.680, 54.884, 0.02],
    'Earth': [1.0, 0.0167, 0.00005, -11.26064, 102.94719, 0.02],
    'Mars': [1.524, 0.0934, 1.850, 49.558, 286.502, 0.015],
    'Jupiter': [5.2, 0.0489, 1.303, 100.464, 273.867, 0.045],
    'Saturn': [9.58, 0.0565, 2.485, 113.665, 339.392, 0.04],
    'Uranus': [19.22, 0.0457, 0.773, 74.006, 96.998, 0.035],
    'Neptune': [30.05, 0.0113, 1.77, 131.783, 273.187, 0.035],
    'Ceres': [2.77, 0.0758, 10.593, 80.393, 73.597, 0.005],
    'Pluto': [39.48, 0.2488, 17.16, 110.299, 113.763, 0.01],
    'Eris': [67.8, 0.44068, 44.04, 35.95, 151.639, 0.01],
    'Haumea': [43.13, 0.19126, 28.19, 121.9, 239, 0.008],
    'Makemake': [45.79, 0.159, 29, 79, 296, 0.008],
    'Sedna': [506, 0.8459, 11.93, 144.31, 311.46, 0.006]
}

# Create multiple plots for different views and scales
fig = plt.figure(figsize=(18, 12))

# Function to create a solar system plot with specific planets and view distance
def create_system_plot(ax, planet_subset, max_dist, title):
    # Draw Sun
    sun_radius = 0.05
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    sun_x_sphere = sun_radius * np.cos(u) * np.sin(v)
    sun_y_sphere = sun_radius * np.sin(u) * np.sin(v)
    sun_z_sphere = sun_radius * np.cos(v)
    ax.plot_surface(sun_x_sphere, sun_y_sphere, sun_z_sphere, color='yellow', alpha=0.7)
    
    # Plot selected planets
    for i, planet in enumerate([p for p in planet_subset if p in orbital_params]):
        params = orbital_params[planet]
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
        ax.plot(x_rotated, y_rotated, z_rotated, color=planet_colors[planet], linewidth=1.5, alpha=0.7)
        
        # Calculate current position (arbitrary point on orbit for visualization)
        # Different starting positions for each planet to avoid overlap
        planet_theta = (i * 30) % 360  # Use the loop index
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
        
        # Create planet
        planet_radius = 0.1 * radius_factor
        ax.scatter([planet_x_rotated], [planet_y_rotated], [planet_z_rotated], 
                   color=planet_colors[planet], s=100*radius_factor, label=planet)
    
    # Title and labels  
    ax.set_title(title, fontsize=12)
    ax.set_xlabel('X (AU)')
    ax.set_ylabel('Y (AU)')
    ax.set_zlabel('Z (AU)')
    
    # Set limits based on the max distance parameter
    ax.set_xlim(-max_dist, max_dist)
    ax.set_ylim(-max_dist, max_dist)
    ax.set_zlim(-max_dist, max_dist)

# Create four different views of the solar system
ax1 = fig.add_subplot(221, projection='3d')
create_system_plot(ax1, 
                  ['Mercury', 'Venus', 'Earth', 'Mars', 'Ceres'], 
                  3, 
                  "Inner Solar System (Mercury to Mars)")

ax2 = fig.add_subplot(222, projection='3d')
create_system_plot(ax2, 
                  ['Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune'], 
                  35, 
                  "Main Planets (Earth to Neptune)")

ax3 = fig.add_subplot(223, projection='3d')
create_system_plot(ax3, 
                  ['Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Haumea', 'Makemake', 'Eris'], 
                  70, 
                  "Outer Planets and Dwarf Planets")

ax4 = fig.add_subplot(224, projection='3d')
create_system_plot(ax4, 
                  ['Earth', 'Jupiter', 'Neptune', 'Pluto', 'Eris', 'Sedna'], 
                  110, 
                  "Extended Solar System (including Sedna)")

# Create a custom legend for the figure
legend_elements = []
for planet, color in planet_colors.items():
    legend_elements.append(plt.Line2D([0], [0], color=color, lw=2, label=planet))
    
fig.legend(handles=legend_elements, loc='center right', title='Planets and Dwarf Planets')

plt.subplots_adjust(wspace=0.3, hspace=0.3, right=0.85)
plt.suptitle("Multi-scale Views of the Solar System", fontsize=16)
plt.show()

# Optional: Create a separate figure showing all orbits in a single view
def create_full_system_visualization():
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Draw Sun
    sun_radius = 0.05
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    sun_x_sphere = sun_radius * np.cos(u) * np.sin(v)
    sun_y_sphere = sun_radius * np.sin(u) * np.sin(v)
    sun_z_sphere = sun_radius * np.cos(v)
    ax.plot_surface(sun_x_sphere, sun_y_sphere, sun_z_sphere, color='yellow', alpha=0.7)
    
    # Group planets by type for better visualization
    inner_planets = ['Mercury', 'Venus', 'Earth', 'Mars']
    outer_planets = ['Jupiter', 'Saturn', 'Uranus', 'Neptune']
    dwarf_planets = ['Ceres', 'Pluto', 'Eris', 'Haumea', 'Makemake', 'Sedna']
    
    # Process all planets with different line styles based on type
    for i, planet in enumerate(orbital_params.keys()):
        params = orbital_params[planet]
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
        
        # Set line style based on planet type
        if planet in inner_planets:
            linestyle = '-'
            alpha = 0.9
        elif planet in outer_planets:
            linestyle = '-'
            alpha = 0.8
        else:  # dwarf planets
            linestyle = '--'
            alpha = 0.6
            
        # Plot orbit
        ax.plot(x_rotated, y_rotated, z_rotated, color=planet_colors[planet], 
                linewidth=1.5, alpha=alpha, linestyle=linestyle)
        
        # Plot the planet as a point
        planet_theta = (i * 30) % 360
        planet_theta = np.radians(planet_theta)
        
        planet_r = semi_major_axis * (1 - eccentricity**2) / (1 + eccentricity * np.cos(planet_theta))
        planet_x = planet_r * np.cos(planet_theta)
        planet_y = planet_r * np.sin(planet_theta)
        planet_z = 0
        
        # Apply the same rotations to get the planet position
        planet_x_peri = planet_x * np.cos(arg_perihelion) - planet_y * np.sin(arg_perihelion)
        planet_y_peri = planet_x * np.sin(arg_perihelion) + planet_y * np.cos(arg_perihelion)
        planet_z_peri = planet_z
        
        planet_x_inclined = planet_x_peri
        planet_y_inclined = planet_y_peri * np.cos(inclination) - planet_z_peri * np.sin(inclination)
        planet_z_inclined = planet_y_peri * np.sin(inclination) + planet_z_peri * np.cos(inclination)
        
        planet_x_rotated = planet_x_inclined * np.cos(longitude_ascending_node) - planet_y_inclined * np.sin(longitude_ascending_node)
        planet_y_rotated = planet_x_inclined * np.sin(longitude_ascending_node) + planet_y_inclined * np.cos(longitude_ascending_node)
        planet_z_rotated = planet_z_inclined
        
        # Create planet
        ax.scatter([planet_x_rotated], [planet_y_rotated], [planet_z_rotated], 
                   color=planet_colors[planet], s=80*radius_factor)
    
    # Add legend grouped by planet type
    legend_elements = [
        plt.Line2D([0], [0], color='yellow', marker='o', linestyle='none', markersize=10, label='Sun'),
        plt.Line2D([0], [0], color='gray', marker='o', linestyle='-', markersize=5, label='Inner Planets'),
        plt.Line2D([0], [0], color='gray', marker='o', linestyle='-', markersize=5, label='Outer Planets'),
        plt.Line2D([0], [0], color='gray', marker='o', linestyle='--', markersize=5, label='Dwarf Planets')
    ]
    
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.05, 1))
    
    # Create a logarithmic-scaled view to show all orbits
    # Using a logarithmic scale for the axes would distort the shape,
    # so instead we'll just use a view that focuses on inner planets but shows outer ones
    
    # Set boundary to show most planets clearly
    boundary = 50
    ax.set_xlim(-boundary, boundary)
    ax.set_ylim(-boundary, boundary)
    ax.set_zlim(-boundary/5, boundary/5)  # Less range on z-axis to see inclinations better
    
    ax.set_title("Complete Solar System (Sedna's full orbit extends beyond view)", fontsize=14)
    ax.set_xlabel('X (AU)')
    ax.set_ylabel('Y (AU)')
    ax.set_zlabel('Z (AU)')
    
    plt.tight_layout()
    plt.subplots_adjust(right=0.85)
    plt.show()

# Uncomment to create the full system visualization
create_full_system_visualization()