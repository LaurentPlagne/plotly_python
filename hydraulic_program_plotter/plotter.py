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

    # Add the unit program as a step chart
    fig.add_trace(go.Scatter(
        x=np.arange(n_timesteps),
        y=unit_program,
        mode='lines',
        line_shape='hv',
        name='Unit Program'
    ))

    # Add the discrete flow levels as horizontal lines
    for level in discrete_levels:
        fig.add_shape(
            type='line',
            x0=0,
            y0=level,
            x1=n_timesteps - 1,
            y1=level,
            line=dict(
                color='red',
                width=2,
                dash='dash'
            )
        )
        fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='lines',
        line=dict(color='red', width=2, dash='dash'),
        name=f'Discrete Level {level}'
    ))


    fig.update_layout(
        title='Hydraulic Unit Program',
        xaxis_title='Time Step',
        yaxis_title='Water Flow (m^3/s)',
        showlegend=True
    )

    return fig
