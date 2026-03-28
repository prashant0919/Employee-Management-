import os
import numpy as np
import matplotlib.pyplot as plt
from config import Config

def _pad_histories(histories):
    max_len = max(len(h) for h in histories)
    arr = np.full((len(histories), max_len), np.nan, dtype=float)
    for i, hist in enumerate(histories):
        arr[i, :len(hist)] = hist
    return arr

def _mean_std_from_results(results_dict, attr_name):
    out = {}
    for alg_name, metric_list in results_dict.items():
        histories = [getattr(m, attr_name) for m in metric_list]
        arr = _pad_histories(histories)
        mean = np.nanmean(arr, axis=0)
        std = np.nanstd(arr, axis=0, ddof=1) if arr.shape[0] > 1 else np.zeros(arr.shape[1])
        out[alg_name] = (mean, std)
    return out

def _plot_with_band(series_dict, title, ylabel, save_path):
    plt.figure(figsize=(10, 6))
    for alg_name, (mean, std) in series_dict.items():
        x = np.arange(1, len(mean) + 1)
        plt.plot(x, mean, linewidth=2, label=alg_name)
        plt.fill_between(x, mean - std, mean + std, alpha=0.15)
    plt.title(title)
    plt.xlabel("Rounds")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close()

def _plot_histogram_per_algorithm(results_dict, extractor, title, xlabel, save_path):
    plt.figure(figsize=(10, 6))
    for alg_name, metric_list in results_dict.items():
        values = []
        for m in metric_list:
            values.extend(extractor(m))
        plt.hist(values, bins=20, alpha=0.4, label=alg_name)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close()

def generate_plots(results_dict, output_dir=Config.RESULTS_DIR):
    plot_dir = os.path.join(output_dir, "plots")
    os.makedirs(plot_dir, exist_ok=True)

    _plot_with_band(
        _mean_std_from_results(results_dict, "alive_hist"),
        title="Alive Nodes vs Rounds",
        ylabel="Alive Nodes",
        save_path=os.path.join(plot_dir, "alive_nodes_plot.png"),
    )

    _plot_with_band(
        _mean_std_from_results(results_dict, "energy_hist"),
        title="Residual Energy vs Rounds",
        ylabel="Residual Energy (J)",
        save_path=os.path.join(plot_dir, "residual_energy_plot.png"),
    )

    _plot_with_band(
        _mean_std_from_results(results_dict, "packets_bs_cum_hist"),
        title="Cumulative Packets Delivered to BS vs Rounds",
        ylabel="Cumulative Packets",
        save_path=os.path.join(plot_dir, "packets_cumulative_plot.png"),
    )

    _plot_with_band(
        _mean_std_from_results(results_dict, "packets_round_hist"),
        title="Packets Delivered to BS per Round",
        ylabel="Packets / Round",
        save_path=os.path.join(plot_dir, "packets_per_round_plot.png"),
    )

    _plot_with_band(
        _mean_std_from_results(results_dict, "ch_count_hist"),
        title="Cluster Head Count vs Rounds",
        ylabel="Cluster Heads",
        save_path=os.path.join(plot_dir, "cluster_head_count_plot.png"),
    )

    _plot_with_band(
        _mean_std_from_results(results_dict, "fairness_hist"),
        title="Jain Fairness Index of Alive-Node Residual Energy",
        ylabel="Jain Fairness",
        save_path=os.path.join(plot_dir, "fairness_plot.png"),
    )

    _plot_with_band(
        _mean_std_from_results(results_dict, "energy_var_hist"),
        title="Residual Energy Variance of Alive Nodes",
        ylabel="Energy Variance",
        save_path=os.path.join(plot_dir, "energy_variance_plot.png"),
    )

    _plot_histogram_per_algorithm(
        results_dict,
        extractor=lambda m: list(m.death_round_by_node.values()),
        title="Histogram of Node Death Rounds",
        xlabel="Death Round",
        save_path=os.path.join(plot_dir, "death_round_histogram.png"),
    )

    _plot_histogram_per_algorithm(
        results_dict,
        extractor=lambda m: list(m.ch_selection_count.values()),
        title="Cluster Head Duty Distribution per Node",
        xlabel="Number of Times Selected as CH",
        save_path=os.path.join(plot_dir, "ch_duty_histogram.png"),
    )