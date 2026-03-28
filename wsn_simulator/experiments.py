import os
import numpy as np
import pandas as pd

from config import Config
from simulator import WSN_Simulator

class ExperimentRunner:
    def __init__(self, protocols, runs=20, output_dir=Config.RESULTS_DIR):
        self.protocols = protocols
        self.runs = runs
        self.output_dir = output_dir
        self.results = {name: [] for name in protocols.keys()}

        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "per_round"), exist_ok=True)

    @staticmethod
    def _summary_stats(values):
        arr = np.asarray(values, dtype=float)
        mean = float(arr.mean())
        std = float(arr.std(ddof=1)) if arr.size > 1 else 0.0
        ci = Config.CI_Z * std / np.sqrt(arr.size) if arr.size > 1 else 0.0
        return mean, std, mean - ci, mean + ci

    @staticmethod
    def _pad_histories(histories, fill_value=np.nan):
        max_len = max(len(h) for h in histories)
        out = np.full((len(histories), max_len), fill_value, dtype=float)
        for i, hist in enumerate(histories):
            out[i, :len(hist)] = hist
        return out

    def execute(self):
        for name, func in self.protocols.items():
            for seed in range(self.runs):
                if hasattr(func, "reset_state"):
                    func.reset_state()

                metrics = WSN_Simulator(seed=seed, protocol_func=func).run()
                self.results[name].append(metrics)

        self._export_per_seed_summary()
        self._export_aggregate_summary()
        self._export_roundwise_metrics()
        return self.results

    def _export_per_seed_summary(self):
        rows = []
        for alg_name, metric_list in self.results.items():
            for seed, m in enumerate(metric_list):
                rows.append({
                    "Algorithm": alg_name,
                    "Seed": seed,
                    "FND": m.fnd,
                    "HND": m.hnd,
                    "LND": m.lnd,
                    "GDW": m.lnd - m.fnd if m.lnd is not None and m.fnd is not None else 0,
                    "TotalPacketsToBS": m.total_packets_to_bs,
                    "FinalResidualEnergy": m.energy_hist[-1] if m.energy_hist else 0.0,
                    "FinalFairnessAlive": m.fairness_hist[-1] if m.fairness_hist else 0.0,
                })

        pd.DataFrame(rows).to_csv(
            os.path.join(self.output_dir, "per_seed_summary.csv"),
            index=False
        )

    def _export_aggregate_summary(self):
        rows = []

        for alg_name, metric_list in self.results.items():
            fnd_vals = [m.fnd if m.fnd is not None else Config.MAX_ROUNDS for m in metric_list]
            hnd_vals = [m.hnd if m.hnd is not None else Config.MAX_ROUNDS for m in metric_list]
            lnd_vals = [m.lnd if m.lnd is not None else Config.MAX_ROUNDS for m in metric_list]
            gdw_vals = [(l - f) for l, f in zip(lnd_vals, fnd_vals)]
            pkt_vals = [m.total_packets_to_bs for m in metric_list]

            fnd_mean, fnd_std, fnd_ci_lo, fnd_ci_hi = self._summary_stats(fnd_vals)
            hnd_mean, hnd_std, hnd_ci_lo, hnd_ci_hi = self._summary_stats(hnd_vals)
            lnd_mean, lnd_std, lnd_ci_lo, lnd_ci_hi = self._summary_stats(lnd_vals)
            gdw_mean, gdw_std, gdw_ci_lo, gdw_ci_hi = self._summary_stats(gdw_vals)
            pkt_mean, pkt_std, pkt_ci_lo, pkt_ci_hi = self._summary_stats(pkt_vals)

            rows.append({
                "Algorithm": alg_name,
                "Mean FND": fnd_mean,
                "Std FND": fnd_std,
                "95CI FND Low": fnd_ci_lo,
                "95CI FND High": fnd_ci_hi,
                "Mean HND": hnd_mean,
                "Std HND": hnd_std,
                "95CI HND Low": hnd_ci_lo,
                "95CI HND High": hnd_ci_hi,
                "Mean LND": lnd_mean,
                "Std LND": lnd_std,
                "95CI LND Low": lnd_ci_lo,
                "95CI LND High": lnd_ci_hi,
                "Mean GDW": gdw_mean,
                "Std GDW": gdw_std,
                "95CI GDW Low": gdw_ci_lo,
                "95CI GDW High": gdw_ci_hi,
                "Mean TotalPacketsToBS": pkt_mean,
                "Std TotalPacketsToBS": pkt_std,
                "95CI Packets Low": pkt_ci_lo,
                "95CI Packets High": pkt_ci_hi,
            })

        df = pd.DataFrame(rows)
        df.to_csv(os.path.join(self.output_dir, "summary_results.csv"), index=False)
        self.summary_df = df

    def _export_one_roundwise_metric(self, alg_name, metric_list, attr_name, csv_name):
        histories = [getattr(m, attr_name) for m in metric_list]
        arr = self._pad_histories(histories, fill_value=np.nan)

        df = pd.DataFrame({
            "Round": np.arange(1, arr.shape[1] + 1),
            "Mean": np.nanmean(arr, axis=0),
            "Std": np.nanstd(arr, axis=0, ddof=1) if arr.shape[0] > 1 else np.zeros(arr.shape[1]),
        })

        df.to_csv(
            os.path.join(self.output_dir, "per_round", f"{alg_name}_{csv_name}.csv"),
            index=False
        )

    def _export_roundwise_metrics(self):
        metric_map = {
            "alive_hist": "alive_nodes",
            "energy_hist": "residual_energy",
            "packets_round_hist": "packets_per_round",
            "packets_bs_cum_hist": "packets_cumulative",
            "ch_count_hist": "cluster_head_count",
            "fairness_hist": "jain_fairness_alive",
            "energy_var_hist": "energy_variance_alive",
        }

        for alg_name, metric_list in self.results.items():
            for attr_name, csv_name in metric_map.items():
                self._export_one_roundwise_metric(alg_name, metric_list, attr_name, csv_name)

            death_rows = []
            ch_rows = []

            for seed, m in enumerate(metric_list):
                for node_id, death_round in m.death_round_by_node.items():
                    death_rows.append({
                        "Algorithm": alg_name,
                        "Seed": seed,
                        "NodeID": node_id,
                        "DeathRound": death_round,
                    })

                for node_id, ch_count in m.ch_selection_count.items():
                    ch_rows.append({
                        "Algorithm": alg_name,
                        "Seed": seed,
                        "NodeID": node_id,
                        "CHSelections": ch_count,
                    })

            pd.DataFrame(death_rows).to_csv(
                os.path.join(self.output_dir, "per_round", f"{alg_name}_death_rounds.csv"),
                index=False
            )
            pd.DataFrame(ch_rows).to_csv(
                os.path.join(self.output_dir, "per_round", f"{alg_name}_ch_frequency.csv"),
                index=False
            )

    def print_summary(self):
        if not hasattr(self, "summary_df"):
            return

        cols = ["Algorithm", "Mean FND", "Std FND", "Mean HND", "Std HND", "Mean LND", "Std LND", "Mean GDW", "Std GDW"]
        print("\n" + self.summary_df[cols].to_string(index=False))