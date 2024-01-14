import os
import re

comment = os.getenv("PR_COMMENT", "")
match = re.search("/wandb[\s+](\S+)", comment)

with open(os.environ["GITHUB_OUTPUT"], "a") as output:
    if match:
        print("DO_COMPARISON=true", file=output)
        print(f"RUN_ID={match.group(1)}", file=output)
    else:
        print("DO_COMPARISON=false", file=output)
