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
    fig.add_hrect(y0=max_discrete, y1=max_discrete + 10, fillcolor="lightcoral", opacity=0.5, layer="below", line_width=0)
    fig.add_hrect(y0=min_discrete - 10, y1=min_discrete, fillcolor="lightcoral", opacity=0.5, layer="below", line_width=0)

    # Add the discrete flow levels as horizontal lines
    for level in discrete_levels:
        fig.add_shape(
            type='line',
            x0=0,
            y0=level,
            x1=n_timesteps,
            y1=level,
            line=dict(
                color='gray',
                width=2,
                dash='dash'
            )
        )

    # Add vertical lines to distinguish time steps
    for i in range(1, n_timesteps):
        fig.add_vline(x=i, line_width=1, line_dash="dash", line_color="lightgrey")

    # Add the unit program as a single trace
    x_values = list(range(n_timesteps + 1))
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
