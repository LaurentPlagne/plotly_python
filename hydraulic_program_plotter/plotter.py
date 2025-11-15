import plotly.graph_objects as go
import numpy as np

def plot_unit_program(unit_program, discrete_levels, n_timesteps):
    """
    Generates a plot of the unit program and discrete flow levels.

    Args:
        unit_program (list or np.ndarray): A series of flow levels for each time step.
        discrete_levels (list or np.ndarray): The discrete flow levels of the unit.
        n_timesteps (int): The number of time steps.

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

    # Add the unit program as a step chart
    fig.add_trace(go.Scatter(
        x=x_coords,
        y=y_coords,
        mode='lines+markers',
        name='Unit Program'
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

    fig.update_layout(
        title='Hydraulic Unit Program',
        xaxis_title='Time Step',
        yaxis_title='Water Flow (m^3/s)',
        showlegend=False
    )

    return fig

if __name__ == '__main__':
    # Example Usage
    n_timesteps = 24
    unit_program = [10, 10, 20, 30, 30, 30, 20, 20, 10, 10, 10, 0, 0, 0, 0, 10, 20, 30, 40, 40, 40, 30, 20, 10]
    discrete_levels = [0, 10, 20, 30, 40]

    fig = plot_unit_program(unit_program, discrete_levels, n_timesteps)
    fig.write_html("hydraulic_unit_program.html")
