# Compares two runs in W&B. A lot is hardcoded/assumed for toy assignment.
import os

import wandb
import wandb.apis.reports as wr

WANDB_ENTITY = "pcowperthwaite"
WANDB_PROJECT = "cicd_assignment"
WANDB_TAG = "baseline"


def compare_runs(run_id: str) -> None:
    if not run_id:
        raise ValueError("No run_id provided.")

    """Compare two runs in W&B."""
    api = wandb.Api()
    baseline_run = api.runs(
        f"{WANDB_ENTITY}/{WANDB_PROJECT}", {"tags": {"$in": [WANDB_TAG]}}
    )[0]

    report = wr.Report(
        entity=WANDB_ENTITY,
        project=WANDB_PROJECT,
        title="Compare Runs.",
        description=f"Comparison of provided run {run_id} and baseline run {baseline_run.id}",
    )

    runs_to_compare = wr.Runset(
        WANDB_ENTITY, WANDB_PROJECT, "Run Comparison"
    ).set_filters_with_python_expr(f"ID in ['{run_id}', '{baseline_run.id}']")
    report_panels = wr.RunComparer(diff_only="split")

    report_grid = wr.PanelGrid(runsets=[runs_to_compare], panels=[report_panels])
    report.blocks = report.blocks[:1] + [report_grid] + report.blocks[1:]
    report.save()

    os.environ["GITHUB_OUTPUT"] = f"REPORT_URL={report.url}"


if __name__ == "__main__":
    compare_runs(os.getenv("RUN_ID", ""))
