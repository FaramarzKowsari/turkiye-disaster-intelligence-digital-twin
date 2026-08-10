# Live Data Layer — v0.1

## Purpose

This milestone turns the repository from a scaffold into a visible, live-data digital-twin prototype.

## Live sources

### AFAD
The application queries AFAD's public earthquake filtering service and normalises heterogeneous
records into a stable internal schema.

### OpenStreetMap
OSMnx retrieves:

- a drivable road network for one İstanbul pilot district,
- hospitals,
- clinics,
- fire stations.

The public deployment intentionally works at district scale to avoid repeatedly downloading the
entire İstanbul graph from Overpass. A city-wide graph will later be preprocessed, versioned and
served as a cached research artifact.

## What the map means

The current map visualises:

- road connectivity,
- selected emergency facilities,
- AFAD catalogue events in the İstanbul bounding region.

It does **not** visualise:

- actual road damage,
- building collapse,
- casualty estimates,
- official resource availability,
- official emergency routing.

Those layers require calibrated data and validated models.

## Next scientific milestone

The next milestone is a reproducible post-earthquake scenario engine:

1. define hazard intensity proxy,
2. derive transparent edge-disruption probabilities,
3. sample Monte Carlo road-failure scenarios,
4. generate incident demand,
5. compare greedy and minimum-cost assignment,
6. quantify uncertainty and fairness.
