import argparse
from protocols import *
from experiments import ExperimentRunner
from plotting import generate_plots
from config import Config

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=20)
    args = parser.parse_args()

    protocols = {
        "LEACH": run_leach_round,
        "DEEC": run_deec_round,
        "HEED": run_heed_round,
        "Proposed": run_proposed_round,
    }

    runner = ExperimentRunner(protocols=protocols, runs=args.runs, output_dir=Config.RESULTS_DIR)
    results = runner.execute()
    runner.print_summary()
    generate_plots(results, output_dir=Config.RESULTS_DIR)

    print(f"\nSaved outputs under: {Config.RESULTS_DIR}/")

if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore")
    main()