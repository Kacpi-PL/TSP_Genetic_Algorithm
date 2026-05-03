import matplotlib.pyplot as plt

def draw_map(x_coords, y_coords, gen):
    fig_map, ax_map = plt.subplots(figsize=(6, 5))
    ax_map.plot(
        x_coords, y_coords, marker="o", linestyle="-", color="#1f77b4", markersize=4
    )
    ax_map.plot(
        x_coords[0], y_coords[0], marker="s", color="red", markersize=8, label="Start"
    )
    ax_map.set_title(f"Route - Generation {gen + 1}")
    ax_map.grid(True, linestyle="--", alpha=0.5)
    ax_map.legend()
    return fig_map

def draw_plot(gen_history, fittest_history, optimum_value):
    fig_plot, ax_plot = plt.subplots(figsize=(6, 5))
    ax_plot.plot(
        gen_history,
        fittest_history,
        color="green",
        linewidth=2,
        label="Best Individual",
    )
    ax_plot.set_xlabel("Generations")
    ax_plot.set_ylabel("Route distance")
    ax_plot.set_title("Distance Convergence Over Time")
    ax_plot.grid(True, linestyle=":", alpha=0.7)
    ax_plot.axhline(
        y=optimum_value, color="r", linestyle="--", label=f"Optimum ({optimum_value})"
    )
    ax_plot.legend()
    return fig_plot