import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

# Constants
a = 1  # Lattice constant

# Create the FCC lattice points
def create_fcc_lattice(num_cells):
    positions = []
    for i in range(num_cells):
        for j in range(num_cells):
            for k in range(num_cells):
                positions.append([i * a, j * a, k * a])  # Corner atoms
                positions.append([i * a + a/2, j * a + a/2, k * a])  # Face-centered atoms
                positions.append([i * a + a/2, j * a, k * a + a/2])
                positions.append([i * a, j * a + a/2, k * a + a/2])
    return np.array(positions)

# Number of unit cells in each direction
num_cells = 4
fcc_positions = create_fcc_lattice(num_cells)

# Create the wave in [111] direction
def wave_displacement(position, k, omega, t):
    # Wavevector in the [111] direction
    k_vector = k * np.array([1, 1, 1]) / np.sqrt(3)
    return np.sin(np.dot(k_vector, position) - omega * t)

# Parameters
k = 2 * np.pi / a  # Wavevector magnitude
omega = 2 * np.pi  # Frequency
time_steps = np.linspace(0, 2 * np.pi, 100)  # Time steps for animation

# Initial time step
t_init = time_steps[0]
displacements_init = [wave_displacement(pos, k, omega, t_init) for pos in fcc_positions]
displaced_positions_init = fcc_positions + np.outer(displacements_init, np.array([1, 1, 1]) / np.sqrt(3))

# Set up the figure for interactive 3D plot
fig = go.Figure()

# Create the initial scatter plot for lattice
fig.add_trace(go.Scatter3d(
    x=displaced_positions_init[:, 0],
    y=displaced_positions_init[:, 1],
    z=displaced_positions_init[:, 2],
    mode='markers',
    marker=dict(size=5, color=displacements_init, colorscale='Viridis', opacity=0.8)
))

# Add a stationary arrow to represent the [111] direction
# Arrow starts at the origin (0, 0, 0) and points in the [111] direction.
arrow_length = 5  # Length of the arrow in arbitrary units
arrow_start = np.array([0, 0, 0])
arrow_end = np.array([1, 1, 1]) / np.sqrt(3) * arrow_length  # Normalize [111] direction

# Add the arrow to the plot as a line trace
fig.add_trace(go.Scatter3d(
    x=[arrow_start[0], arrow_end[0]],
    y=[arrow_start[1], arrow_end[1]],
    z=[arrow_start[2], arrow_end[2]],
    mode='lines',
    line=dict(color='red', width=5),
    name='[111] Direction'
))

# Create animation frames
frames = []
for t in time_steps:
    displacements = [wave_displacement(pos, k, omega, t) for pos in fcc_positions]
    displaced_positions = fcc_positions + np.outer(displacements, np.array([1, 1, 1]) / np.sqrt(3))
    
    frames.append(go.Frame(data=[go.Scatter3d(
        x=displaced_positions[:, 0],
        y=displaced_positions[:, 1],
        z=displaced_positions[:, 2],
        mode='markers',
        marker=dict(size=5, color=displacements, colorscale='Viridis', opacity=0.8)
    )], name=f"Time = {t:.2f}"))

# Add frames to the figure
fig.frames = frames

# Animation settings and layout
fig.update_layout(
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z',
        aspectmode='cube'
    ),
    title="3D FCC Lattice with Wave Propagation and [111] Direction",
    updatemenus=[dict(type="buttons",
                      showactive=False,
                      buttons=[dict(label="Play",
                                    method="animate",
                                    args=[None, {"frame": {"duration": 50, "redraw": True}, 
                                                 "fromcurrent": True, "mode": "immediate"}]),
                               dict(label="Pause",
                                    method="animate",
                                    args=[[None], {"frame": {"duration": 0, "redraw": False}, 
                                                   "mode": "immediate"}])
                              ])]
)

# Show the interactive plot
pio.show(fig)

