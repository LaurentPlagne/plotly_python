import plotly.graph_objects as go
import numpy as np

def plot_unit_program(unit_program, discrete_levels, n_timesteps, forbidden_levels=None):
    """
    Generates a plot of the unit program and discrete flow levels.

    Args:
        unit_program (list or np.ndarray): A series of flow levels for each time step.
        discrete_levels (list or np.ndarray): The discrete flow levels of the unit.
        n_timesteps (int): The number of time steps.
        forbidden_levels (dict, optional): A dictionary where keys are time steps and
                                           values are lists of forbidden flow levels.
                                           Defaults to None.
    Returns:
        go.Figure: The Plotly figure object.
    """
    fig = go.Figure()

    # Prepare data for horizontal steps
    x_coords = []
    y_coords = []
    for i in range(n_timesteps):
        x_coords.extend([i, i + 1])
        y_coords.extend([unit_program[i], unit_program[i]])
        if i < n_timesteps - 1:
            x_coords.append(None)
            y_coords.append(None)

    # Add the unit program as a step chart with a thicker line
    fig.add_trace(go.Scatter(
        x=x_coords,
        y=y_coords,
        mode='lines+markers',
        name='Unit Program',
        line=dict(width=4)  # Make the line thicker
    ))

    # Add the discrete flow levels as horizontal lines
    for level in discrete_levels:
        fig.add_shape(
            type='line',
            x0=0,
            y0=level,
            x1=n_timesteps,
            y1=level,
            line=dict(
                color='red',
                width=2,
                dash='dash'
            )
        )

    # Add markers for forbidden levels
    if forbidden_levels:
        forbidden_x = []
        forbidden_y = []
        for timestep, levels in forbidden_levels.items():
            for level in levels:
                # Place the marker in the middle of the time step
                forbidden_x.append(timestep + 0.5)
                forbidden_y.append(level)

        fig.add_trace(go.Scatter(
            x=forbidden_x,
            y=forbidden_y,
            mode='markers',
            name='Forbidden Level',
            marker=dict(
                color='red',
                symbol='x',
                size=10
            )
        ))

    fig.update_layout(
        title='Hydraulic Unit Program',
        xaxis_title='Time Step',
        yaxis_title='Water Flow (m^3/s)',
        showlegend=False,
        xaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=1,
            minor=dict(
                ticklen=6,
            )
        )
    )

    return fig

if __name__ == '__main__':
    # Example Usage
    n_timesteps = 24
    # Include a non-discrete value (e.g., 25)
    unit_program = [10, 10, 20, 30, 30, 30, 20, 25, 10, 10, 10, 0, 0, 0, 0, 10, 20, 30, 40, 40, 40, 30, 20, 10]
    discrete_levels = [0, 10, 20, 30, 40]
    # Define forbidden levels for specific time steps
    forbidden_levels = {
        1: [20, 30],
        2: [0, 10],
        7: [0, 10, 20, 30, 40]
    }

    fig = plot_unit_program(unit_program, discrete_levels, n_timesteps, forbidden_levels)
    fig.write_html("hydraulic_unit_program.html")
