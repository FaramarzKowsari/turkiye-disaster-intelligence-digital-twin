# Coupled Phase Boundary Benchmark #3 — Reproducible Evidence

GitHub Actions run: `31545788832`  
Artifact ID: `9122652977`  
Artifact: `disaster-twin-coupled-phase-boundary-31545788832-attempt-1`  
Source commit: `b485feb9d154e8ccc38ba593a5d36069052d408c`  
Pilot area: `Beykoz, İstanbul, Türkiye`  
Realisations: `100`  
Raw algorithm-level observations: `12,800`  
Artifact SHA-256: `547c0a2d1277bf7891b308a623c2e6dc879d59c1d9ff236547473230bf9f5b5f`

## English

The coupled v0.6 benchmark removed the local severity-frontier reversal observed in the earlier
independent-world design. For Global Minimum-Cost Assignment, the 80% reachability / 80%
reliability frontier was:

| Severity | Minimum responders |
|---:|---:|
| 0.10 | 10 |
| 0.12 | 10 |
| 0.13 | 12 |
| 0.14 | 14 |
| 0.15 | 14 |
| 0.16 | not reached ≤32 |
| 0.18 | not reached ≤32 |
| 0.20 | not reached ≤32 |

The Global algorithm produced **0 reachability-increase violations across
800 complete responder/world trajectories**. The Greedy heuristic produced
3 local violations across 800 trajectories, which is compatible
with path removal changing the heuristic's sequential choices.

At 32 responders, Global service-target probability declined monotonically from 97% at severity
0.10 to 59% at 0.20. The tested 80/80 frontier remained feasible through severity 0.15 but was no
longer reached at 0.16, motivating the high-resolution v0.7 confirmatory study.

All 11 internal SHA-256 checksums in the preserved artifact were independently
verified before inclusion.

## Türkçe

Eşleştirilmiş v0.6 benchmark, önceki bağımsız rastgele dünya tasarımında görülen yerel şiddet
terslenmesini ortadan kaldırdı. Global Minimum-Cost Assignment için 80/80 hizmet sınırı 0.15'e
kadar karşılandı; 0.16 ve üzerindeki test edilmiş şiddetlerde 32 ekip ile bile karşılanmadı.

Global algoritmada 800 tam yörüngede şiddet arttıkça erişilebilirliğin yükseldiği
hiçbir ihlal görülmedi. Bu sonuç v0.7'nin 0.13–0.165 aralığında daha yüksek çözünürlüklü doğrulayıcı
bir sınır çalışmasına geçmesini desteklemektedir.

## Español (España)

El benchmark acoplado v0.6 eliminó la inversión local de la frontera observada con mundos
aleatorios independientes. Para la Asignación Global de Coste Mínimo, el criterio 80/80 se mantuvo
hasta la severidad 0,15 y dejó de alcanzarse a partir de 0,16 incluso con 32 recursos.

No se observó ninguna violación de aumento de accesibilidad con mayor severidad en las
800 trayectorias completas del algoritmo Global. Este resultado justifica el
estudio confirmatorio v0.7 con mayor resolución alrededor de la frontera.
