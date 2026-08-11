# Benchmark #1 — Reproducible Results

GitHub Actions run: `31483492277`  
Source commit: `163aa59f0745051ba67b2e4786b76081546ece3b`  
Pilot area: `Beykoz, İstanbul, Türkiye`  
Realisations per severity: `100`  
Synthetic severities: `0.10, 0.25, 0.40`  
Incidents: `10`  
Responders: `8`  
Base seed: `2026`

## English

The first paper-grade benchmark produced 600 algorithm-level observations from 300 matched
synthetic scenarios. The Global Minimum-Cost Assignment reduced total response time relative to
the sequential Greedy baseline by approximately:

| Severity | Greedy mean total response (s) | Global mean total response (s) | Reduction |
|---:|---:|---:|---:|
| 0.10 | 6188.21 | 4556.04 | 26.4% |
| 0.25 | 2338.42 | 1934.28 | 17.3% |
| 0.40 | 440.80 | 400.23 | 9.2% |

For total response time, the paired bootstrap confidence interval for Greedy minus Global remained
above zero at all three severities, with Holm-adjusted permutation p-values of 0.0003, 0.0003 and
0.0010 respectively.

However, mean reachability changed very little:

- severity 0.10: 74.2% Greedy vs 74.3% Global,
- severity 0.25: 35.6% vs 35.8%,
- severity 0.40: 11.2% vs 11.2%.

Weighted unmet demand showed no statistically meaningful algorithm difference. At severity 0.40,
32 of 100 realisations had no reachable assignment at all, and the two algorithms tied on total
response time in 88% of paired scenarios.

**Interpretation:** optimisation improves the allocation cost of reachable resources, but once
network connectivity and resource access collapse, allocation quality alone cannot restore service.

Cross-severity total-response means must not be interpreted as "higher severity is faster":
severe scenarios often have fewer reachable incidents, so total travel time can fall while service
quality collapses.

## Türkçe

İlk makale düzeyindeki benchmark, 300 eşleştirilmiş sentetik senaryodan 600 algoritma düzeyi gözlem
üretti. Küresel Minimum Maliyetli Atama, sıralı Greedy yönteme kıyasla toplam müdahale süresini
0.10 şiddetinde yaklaşık %26,4; 0.25'te %17,3; 0.40'ta %9,2 azalttı.

Buna karşın erişilebilirlik neredeyse değişmedi: sırasıyla %74,2→%74,3, %35,6→%35,8 ve
%11,2→%11,2. Ağırlıklı karşılanamayan talepte anlamlı algoritma farkı görülmedi.

0.40 şiddetinde 100 gerçekleşmenin 32'sinde hiçbir erişilebilir atama yoktu ve toplam müdahale
süresinde senaryoların %88'inde iki algoritma eşit kaldı.

**Yorum:** optimizasyon erişilebilir kaynakların tahsis maliyetini iyileştirir; ancak bağlantılılık
ve kaynak erişimi çöktüğünde yalnızca daha iyi tahsis hizmeti geri getiremez.

## Español (España)

El primer benchmark con calidad de publicación generó 600 observaciones algorítmicas a partir de
300 escenarios sintéticos emparejados. La Asignación Global de Coste Mínimo redujo el tiempo total
de respuesta frente al método Greedy aproximadamente un 26,4% con severidad 0,10, un 17,3% con
0,25 y un 9,2% con 0,40.

La accesibilidad, sin embargo, apenas cambió: 74,2%→74,3%, 35,6%→35,8% y 11,2%→11,2%.
La demanda ponderada no atendida no mostró una diferencia algorítmica estadísticamente relevante.

Con severidad 0,40, 32 de las 100 realizaciones no permitieron ninguna asignación alcanzable y
ambos algoritmos empataron en tiempo total de respuesta en el 88% de los escenarios emparejados.

**Interpretación:** la optimización mejora el coste de asignación de los recursos que siguen siendo
alcanzables; cuando colapsan la conectividad y el acceso a recursos, una mejor asignación por sí
sola no puede recuperar el servicio.
