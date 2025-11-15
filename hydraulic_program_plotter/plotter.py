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

    min_discrete = min(discrete_levels)
    max_discrete = max(discrete_levels)

    # Add shaded regions for invalid flow levels
    fig.add_hrect(y0=max_discrete, y1=max_discrete + 10, fillcolor="lightgray", opacity=0.3, layer="below", line_width=0)
    fig.add_hrect(y0=min_discrete - 10, y1=min_discrete, fillcolor="lightgray", opacity=0.3, layer="below", line_width=0)

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

    # Segment the program into valid and invalid parts for coloring
    segments = []
    current_x = []
    current_y = []
    current_color = None
    discrete_set = set(discrete_levels)

    for i in range(n_timesteps):
        y = unit_program[i]
        is_valid = y in discrete_set
        color = 'blue' if is_valid else 'red'

        if current_color is None:
            current_color = color

        if color != current_color:
            current_x.append(i)
            current_y.append(y)
            segments.append({'x': current_x, 'y': current_y, 'color': current_color})

            current_x = [i]
            current_y = [y]
            current_color = color
        else:
            current_x.append(i)
            current_y.append(y)

    # Add the last segment
    current_x.append(n_timesteps)
    current_y.append(unit_program[-1])
    segments.append({'x': current_x, 'y': current_y, 'color': current_color})

    # Add traces for each segment
    for i, seg in enumerate(segments):
        fig.add_trace(go.Scatter(
            x=seg['x'],
            y=seg['y'],
            mode='lines',
            line_shape='hv',
            line=dict(width=4, color=seg['color']),
            name='Unit Program' if i == 0 else '',
            showlegend= i == 0
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
    n_timesteps = 96
    # Include a non-discrete value (e.g., 25)
    unit_program = [10, 10, 20, 30, 30, 30, 20, 25, 10, 10, 10, 0, 0, 0, 0, 10, 20, 30, 40, 40, 40, 30, 20, 10] * 4
    discrete_levels = [0, 10, 22, 35, 40]

    fig = plot_unit_program(unit_program, discrete_levels, n_timesteps)
    fig.write_html("hydraulic_unit_program.html")
