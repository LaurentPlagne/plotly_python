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

    # Determine the lower and upper bounds for the valid region
    sorted_discrete = np.sort(discrete_levels)
    min_bound = []
    max_bound = []

    for val in unit_program:
        # Find the largest discrete level <= val
        lower = sorted_discrete[sorted_discrete <= val]
        min_bound.append(lower[-1] if len(lower) > 0 else sorted_discrete[0])

        # Find the smallest discrete level >= val
        upper = sorted_discrete[sorted_discrete >= val]
        max_bound.append(upper[0] if len(upper) > 0 else sorted_discrete[-1])

    x_fill = list(range(1, n_timesteps + 1))

    # Add the lower invalid region
    fig.add_trace(go.Scatter(
        x=x_fill + x_fill[::-1],
        y=[min(discrete_levels)] * n_timesteps + min_bound[::-1],
        fill='toself',
        fillcolor='darkgray',
        line=dict(color='darkgray'),
        name='Invalid Region',
        showlegend=False
    ))

    # Add the upper invalid region
    fig.add_trace(go.Scatter(
        x=x_fill + x_fill[::-1],
        y=[max(discrete_levels) + 10] * n_timesteps + max_bound[::-1],
        fill='toself',
        fillcolor='darkgray',
        line=dict(color='darkgray'),
        showlegend=False,
        name='Invalid Region'
    ))

    # Add the discrete flow levels as horizontal lines
    for level in discrete_levels:
        fig.add_shape(
            type='line',
            x0=1,
            y0=level,
            x1=n_timesteps + 1,
            y1=level,
            line=dict(
                color='gray',
                width=2,
                dash='dash'
            )
        )

    # Add vertical lines to distinguish time steps
    for i in range(2, n_timesteps + 1):
        fig.add_vline(x=i, line_width=1, line_dash="dash", line_color="lightgrey")

    # Add the unit program as a single trace
    x_values = list(range(1, n_timesteps + 2))
    y_values = list(unit_program) + [unit_program[-1]]
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines',
        line_shape='hv',
        line=dict(width=4, color='blue'),
        name='Unit Program'
    ))

    fig.update_layout(
        title='Hydraulic Unit Program',
        xaxis_title='Time Step',
        yaxis_title='Water Flow (m^3/s)',
        showlegend=True,
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(1, n_timesteps + 1)),
            ticktext=[str(i) for i in range(1, n_timesteps + 1)]
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
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
