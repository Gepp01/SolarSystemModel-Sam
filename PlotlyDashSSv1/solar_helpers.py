# solar_helpers.py
import numpy as np
import plotly.graph_objects as go

# Shared data
planet_colors = {
    'Mercury': '#8c8680', 'Venus': '#e6c89c', 'Earth': '#4f71be', 'Mars': '#d1603d',
    'Jupiter': '#e0ae6f', 'Saturn': '#c5ab6e', 'Uranus': '#9fc4e7', 'Neptune': '#4f71be',
    'Ceres': '#8c8680', 'Pluto': '#ab9c8a', 'Eris': '#d9d9d9', 'Haumea': '#d9d9d9',
    'Makemake': '#c49e6c', 'Sedna': '#bb5540'
}

orbital_params = {
    'Mercury': [0.387, 0.2056, 7.005, 48.331, 29.124, 0.008],
    'Venus':   [0.723, 0.0068, 3.39458, 76.680, 54.884, 0.02],
    'Earth':   [1.0,   0.0167, 0.00005, -11.26064, 102.94719, 0.02],
    'Mars':    [1.524, 0.0934, 1.850,    49.558,     286.502,   0.015],
    'Jupiter': [5.2,   0.0489, 1.303,    100.464,    273.867,   0.045],
    'Saturn':  [9.58,  0.0565, 2.485,    113.665,    339.392,   0.04],
    'Uranus':  [19.22, 0.0457, 0.773,    74.006,     96.998,    0.035],
    'Neptune':[30.05, 0.0113, 1.77,     131.783,    273.187,   0.035],
    'Ceres':   [2.77,  0.0758, 10.593,   80.393,     73.597,    0.005],
    'Pluto':   [39.48, 0.2488, 17.16,    110.299,    113.763,   0.01],
    'Eris':    [67.8,  0.44068,44.04,    35.95,      151.639,   0.01],
    'Haumea':  [43.13, 0.19126,28.19,    121.9,      239,       0.008],
    'Makemake':[45.79, 0.159,  29,       79,         296,       0.008],
    'Sedna':   [506,   0.8459, 11.93,    144.31,     311.46,    0.006]
}

# Helper: build Plotly traces for a planet list

def make_traces(planet_list):
    traces = []
    # Sun sphere
    u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:15j]
    x_s = 0.05 * np.cos(u) * np.sin(v)
    y_s = 0.05 * np.sin(u) * np.sin(v)
    z_s = 0.05 * np.cos(v)
    traces.append(go.Surface(x=x_s, y=y_s, z=z_s,
                             colorscale=[[0,'yellow'],[1,'yellow']],
                             opacity=0.7, showscale=False))
    # Planets
    for i, name in enumerate(planet_list):
        a,e,inc,Ω,ω,rf = orbital_params[name]
        inc,Ω,ω = np.radians([inc,Ω,ω])
        θ = np.linspace(0,2*np.pi,500)
        r = a*(1-e**2)/(1+e*np.cos(θ))
        x = r*np.cos(θ); y = r*np.sin(θ); z = np.zeros_like(θ)
        # rotate & incline
        x1 = x*np.cos(ω)-y*np.sin(ω)
        y1 = x*np.sin(ω)+y*np.cos(ω)
        y2 = y1*np.cos(inc); z2 = y1*np.sin(inc)
        x3 = x1*np.cos(Ω)-y2*np.sin(Ω)
        y3 = x1*np.sin(Ω)+y2*np.cos(Ω)
        # orbit line
        traces.append(go.Scatter3d(x=x3, y=y3, z=z2, mode='lines',
                                   line=dict(color=planet_colors[name], width=2), showlegend=False))
        # current pos
        t0 = np.radians((i*30)%360)
        r0 = a*(1-e**2)/(1+e*np.cos(t0))
        x0,y0 = r0*np.cos(t0), r0*np.sin(t0)
        x0p = x0*np.cos(ω)-y0*np.sin(ω)
        y0p = x0*np.sin(ω)+y0*np.cos(ω)
        y0i = y0p*np.cos(inc); z0i = y0p*np.sin(inc)
        x0r = x0p*np.cos(Ω)-y0i*np.sin(Ω)
        y0r = x0p*np.sin(Ω)+y0i*np.cos(Ω)
        traces.append(go.Scatter3d(x=[x0r], y=[y0r], z=[z0i],
                                   mode='markers', marker=dict(size=8*rf, color=planet_colors[name]), name=name))
    return traces

# Helper: build a complete figure

def build_fig(subset, rng, title):
    fig = go.Figure(data=make_traces(subset))
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-rng,rng], title='X (AU)'),
            yaxis=dict(range=[-rng,rng], title='Y (AU)'),
            zaxis=dict(range=[-rng,rng], title='Z (AU]'),
            aspectmode='data'
        ),
        margin=dict(l=0,r=0,t=40,b=0), title=title
    )
    return fig