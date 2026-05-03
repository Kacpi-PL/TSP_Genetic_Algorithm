import streamlit as st
import time
import matplotlib.pyplot as plt
import visualization
import json
from tsp_problem import TSPProblem
from genetic_algorithm import GeneticAlgorithm


# -- Dicts --
SEL_MAP = {
    "Tournament Selection": "tournament",
    "Roulette Selection": "roulette",
    "Rank Selection": "rank"
}
CX_MAP = {
    "Ordered Crossover": "ox",
    "Partially Mapped Crossover": "pmx",
    "Edge Recombinantion Crossover": "erx"
}
MUT_MAP = {
    "Inverse Mutation": "inverse",
    "Swap Mutation": "swap",
    "Scramble Mutation": "scramble"
}

# -- Sidebar --
def render_sidebar():
    with st.sidebar:
        st.header("Algorithm Parameters")
        # -- Sliders with params --
        params = {
            "dataset": st.radio("Dataset", ["ATT48", "Berlin52"], horizontal=True),
            "pop_size": st.slider("Population", 100, 1000, 500),
            "generations": st.slider("Generations", 100, 2000, 1000),
            "mut_pb": st.slider("Mutation Probability", 0.00, 1.0, 0.15),
            "cx_pb": st.slider("Crossover Probability", 0.00, 1.0, 0.90),
            "selection": st.selectbox("Selection Operator", list(SEL_MAP.keys())),
            "crossover": st.selectbox("Crossover Operator", list(CX_MAP.keys())),
            "mutation": st.selectbox("Mutation Operator", list(MUT_MAP.keys())),
            "elite_size": st.slider("Elite", 0, 10, 1),
        }
        # -- Start button that launches GA loop --
        start_btn = st.button("START", type="primary", use_container_width=True)
    return params, start_btn

# -- Drawing charts and metrics
def update_dashboard(placeholders, metrics, plots_data):
    top_bar_pl, map_pl, plot_pl = placeholders
    with top_bar_pl.container(border=True):
        col1, col2, col3, col4, col5 = st.columns(5, vertical_alignment="bottom")


        col1.metric("Best distance", f"{metrics['best_dist']:.2f}")
        col2.metric("Diff to Optimum", f"{metrics['diff_optimum']:.2f}")
        col3.metric("Generation", f"{metrics['gen']}/{metrics['total_gens']}")
        col4.metric("Execution time", f"{metrics['time']:.2f} s")
        col5.metric("Improvement", f"{metrics['imprv']:.2f}%")

    fig_map = visualization.draw_map(
        plots_data["x_coords"], plots_data["y_coords"], metrics["gen"]
    )
    map_pl.pyplot(fig_map)
    plt.close(fig_map)


    fig_plot = visualization.draw_plot(
        plots_data["generations"], plots_data["distances"], plots_data["optimum"]
    )
    plot_pl.pyplot(fig_plot)
    plt.close(fig_plot)

# -- GA func
def run_evolution(params):
    top_bar_placeholder = st.empty()
    left, right = st.columns(2)
    map_placeholder = left.empty()
    plot_placeholder = right.empty()
    progress_bar = st.progress(0)
    placeholders = (top_bar_placeholder, map_placeholder, plot_placeholder)
    file_path = f"data/{params['dataset'].lower()}.tsp"
    optimum_value = 10628 if params["dataset"] == "ATT48" else 7542
    try:
        tsp_data = TSPProblem(file_path)
    except Exception as e:
        st.error(f"File loading error {file_path}: {e}")
        st.stop()

    # -- GA with params from sidebar --
    ga = GeneticAlgorithm(
        distance_matrix=tsp_data.dist_matrix,
        pop_size=params["pop_size"],
        selection_type=SEL_MAP[params["selection"]],
        crossover_type=CX_MAP[params["crossover"]],
        mutation_type=MUT_MAP[params["mutation"]],
        elite_size=params["elite_size"],
    )

    all_best_distances = []
    all_generations = []
    nodes = list(tsp_data.problem.get_nodes())
    start_time = time.perf_counter()
    start_dist = None

    # GA generations loop
    for gen in range(params["generations"]):
        best_route, best_dist = ga.run_generation(params["cx_pb"], params["mut_pb"])

        all_best_distances.append(best_dist)
        all_generations.append(gen)

        if gen == 0:
            start_dist = best_dist

        # -- Top bar and columns metrics
        if (
            gen % max(1, (params["generations"] // 50)) == 0
            or gen == params["generations"] - 1
        ):
            current_time = time.perf_counter() - start_time
            imprv = (start_dist - best_dist) / start_dist * 100

            x_coords = [
                tsp_data.problem.node_coords[nodes[node]][0] for node in best_route
            ]
            y_coords = [
                tsp_data.problem.node_coords[nodes[node]][1] for node in best_route
            ]
            x_coords.append(tsp_data.problem.node_coords[nodes[best_route[0]]][0])
            y_coords.append(tsp_data.problem.node_coords[nodes[best_route[0]]][1])

            metrics = {
                "best_dist": best_dist,
                "diff_optimum": best_dist - optimum_value,
                "gen": gen + 1,
                "total_gens": params["generations"],
                "time": current_time,
                "imprv": imprv,
            }

            plots_data = {
                "x_coords": x_coords,
                "y_coords": y_coords,
                "generations": all_generations,
                "distances": all_best_distances,
                "optimum": optimum_value,
            }

            update_dashboard(placeholders, metrics, plots_data)

        progress_bar.progress((gen + 1) / params["generations"])

    total_time = time.perf_counter() - start_time
    imprv_final = (start_dist - best_dist) / start_dist * 100

    st.success(
                f"Complete! Time: {total_time:.2f} s. Best dist.: {best_dist:.2f}"
    )
    if best_dist <= optimum_value:
        st.balloons()

    # Dict with results
    export_data = {
        "dataset": params["dataset"],
        "parameters": params,
        "results": {
            "execution_time_s": round(total_time, 2),
            "start_distance": round(start_dist, 2),
            "best_distance": round(best_dist, 2),
            "optimum_distance": optimum_value,
            "improvement_percent": round(imprv_final, 2),
            "best_route": best_route,
            "distance_history": all_best_distances,
        },
    }

    st.download_button(
        label="Download results (JSON)",
        data=json.dumps(export_data, indent=4),
        file_name=f"raport_TSP_{params['dataset']}_{int(best_dist)}.json",
        mime="application/json",
        use_container_width=True,
    )


def main():
    st.set_page_config(page_title="Genetic Algorithm TSP", layout="wide")

    params, start_btn = render_sidebar()

    if start_btn:
        run_evolution(params)

if __name__ == "__main__":
    main()