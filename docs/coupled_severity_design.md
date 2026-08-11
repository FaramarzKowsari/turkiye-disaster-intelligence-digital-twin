# Coupled Severity Design — v0.6

## Why v0.6 exists

The v0.5 phase-transition study correctly paired resource levels within each severity: lower
responder counts used nested subsets of the same responder pool. However, different severity
levels still used independent random seeds. This is acceptable for estimating each severity in
isolation, but it is inefficient and noisy when the scientific target is the *location of a phase
boundary*.

Benchmark #2 exposed the symptom directly: the 80/80 service frontier failed at severity 0.15 but
reappeared at 0.16. The confidence intervals overlap, so the reversal is consistent with sampling
variation rather than a true improvement at higher disruption.

## Common random numbers on both experimental axes

v0.6 defines one latent stochastic world per realisation:

1. one incident set,
2. one maximum responder pool,
3. one uniform random variate for every directed road edge.

All responder-count conditions use nested prefixes of the same responder pool. All severity
conditions use the same edge-level uniform variates. The synthetic failure probability changes with
severity, but the random draw does not.

Therefore, if an edge fails at severity `s`, it must also fail at every larger tested severity.
Synthetic failed-edge sets are mathematically nested.

For Global Minimum-Cost Assignment, maximum reachable assignment cardinality can therefore only
stay equal or decrease as severity rises for the same seed and responder count. This removes a
major source of Monte Carlo noise from phase-boundary estimation.

## What remains synthetic

The coupling improves experimental design; it does not turn the disruption field into an
engineering fragility model. Severity is still a controlled stress-test parameter, not an official
road-damage probability, earthquake forecast or operational emergency recommendation.

## Türkçe özet

v0.6 her gerçekleşme için olayları, maksimum müdahale ekibi havuzunu ve yol kenarlarına ait rastgele
sayıları bütün şiddet düzeylerinde sabit tutar. Şiddet arttıkça yalnızca eşik değişir; bu nedenle
kesilen yol kenarları iç içe geçmiş kümeler oluşturur. Böylece 0.15 ve 0.16 gibi komşu şiddetleri
farklı rastgele dünyalarla karşılaştırmaktan doğan gürültü önemli ölçüde azalır.

## Resumen en español

La v0.6 mantiene, para cada realización, los mismos incidentes, el mismo conjunto máximo de recursos
y los mismos números aleatorios asociados a cada arista en todos los niveles de severidad. Al
aumentar la severidad solo cambia el umbral de fallo, por lo que los conjuntos de aristas
interrumpidas quedan anidados. Esto reduce de forma importante el ruido Monte Carlo al estimar la
frontera de transición.
