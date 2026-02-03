"""CLI entrypoint for the Placement Intelligence System."""
from __future__ import annotations

import argparse
from pathlib import Path

from placement.data import load_dataset, ensure_valid
from placement.dashboard import build_dashboard_metrics
from placement.fraud import flag_suspicious_offers, summarize_suspicious_offers
from placement.model import train_model, add_predictions
from placement.report import ReportPayload, render_report, write_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to placement CSV data.")
    parser.add_argument(
        "--report",
        required=True,
        help="Path to write the markdown report.",
    )
    parser.add_argument(
        "--z-threshold",
        type=float,
        default=2.5,
        help="Z-score threshold for suspicious offer detection.",
    )
    parser.add_argument(
        "--notes",
        default="Generated automatically by the placement intelligence system.",
        help="Notes to append to the report.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset = load_dataset(args.input)
    frame = ensure_valid(dataset)

    model = train_model(frame)
    scored = add_predictions(frame, model)

    flagged = flag_suspicious_offers(scored, z_threshold=args.z_threshold)
    metrics = build_dashboard_metrics(flagged)
    suspicious_offers = summarize_suspicious_offers(flagged)

    report_content = render_report(
        ReportPayload(
            metrics=metrics,
            suspicious_offers=suspicious_offers,
            notes=args.notes,
        )
    )

    write_report(report_content, Path(args.report))


if __name__ == "__main__":
    main()
