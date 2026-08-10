# EdgeRisk backward-compatibility test hotfix

The v0.2 scenario engine introduced `distance_km` on `EdgeRisk`, while the original
v0.1 tests still construct `EdgeRisk(edge_id, failure_probability)`.

This patch makes:

`distance_km: float = 0.0`

so the old API remains valid.

It also generalises `edge_id` to `Hashable`, matching the original test contract.
New graph-generated risks still explicitly store `(u, v, key)` tuples and the
actual calculated distance.

## Apply

Extract into the repository root and replace:

`src/turkiye_disaster_twin/simulation/scenario.py`

Commit with:

`Restore EdgeRisk backward compatibility`

Then push to `main`.
