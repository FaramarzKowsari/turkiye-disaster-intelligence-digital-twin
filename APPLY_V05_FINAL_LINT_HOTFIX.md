# v0.5 final CI lint hotfix

GitHub Actions reports one remaining Ruff error:

`F401: numpy imported but unused`

This patch removes only `import numpy as np` from:

`src/turkiye_disaster_twin/simulation/phase_transition.py`

No algorithmic or statistical behavior changes.

Commit message:

`Remove final unused numpy import in v0.5`
