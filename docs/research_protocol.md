# Research Protocol — v0.1

## Primary research question

Under uncertain post-earthquake road disruption and emergency demand in İstanbul,
can graph-aware resource allocation improve response performance compared with
transparent static baselines?

## Null hypothesis

Graph-aware optimization does not significantly improve response time, reachability,
or weighted unmet demand compared with a nearest-responder baseline under matched
scenario conditions.

## Independent variables

- earthquake scenario
- road-disruption probability
- number and spatial distribution of incidents
- number of responders
- responder pre-positioning
- hospital capacity
- observation uncertainty

## Dependent variables

- mean / median / p90 response time
- weighted unmet demand
- reachable incident fraction
- hospital overload
- total travel time
- district fairness gap
- network resilience ratio

## Experimental design

For each scenario family:

1. Generate N stochastic road-disruption realizations.
2. Generate incident demand with a fixed random seed schedule.
3. Evaluate identical scenarios with all baseline policies.
4. Store raw episode-level outputs.
5. Report confidence intervals, not only point estimates.
6. Perform sensitivity analysis over disruption severity and fleet size.

## Baselines

B0 — nearest responder, no capacity model  
B1 — travel-time greedy  
B2 — minimum-cost capacitated assignment  
B3 — static robust pre-positioning heuristic  
B4 — learned policy (future MARL phase)

## Non-negotiable scientific rules

- no cherry-picked scenarios,
- every random experiment stores its seed,
- synthetic variables are labeled synthetic,
- learned methods must beat transparent baselines,
- failures and negative results are reported.

## Phase-gate to RL

Do not begin MARL until:
- graph construction is stable,
- scenario generator is tested,
- at least three baselines are implemented,
- metrics are fixed,
- experiment logging is reproducible.
