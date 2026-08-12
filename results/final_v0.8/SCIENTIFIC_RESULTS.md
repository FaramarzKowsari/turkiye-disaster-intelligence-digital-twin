# Scientific Results Freeze — v0.8

## English

### Primary confirmatory result

The final Beykoz confirmatory analysis estimates the synthetic **80/80 reliability boundary**:
the disruption-severity control value at which the probability of retaining at least 80%
incident reachability crosses 80%.

| Responders | Boundary estimate | 95% world-bootstrap interval |
|---:|---:|---:|
| 12 | 0.142500 | 0.134000–0.148462 |
| 14 | 0.149167 | 0.142500–0.156000 |
| 16 | 0.152500 | 0.145333–0.160000 |
| 20 | 0.154500 | 0.147000–0.163214 |
| 24 | 0.158333 | 0.148462–0.168214 |
| 32 | 0.162500 | 0.154167–0.172727 |

The boundary moves upward as responder availability increases, but the gains are not linear.
Across the tested resource range, the point estimate rises from
**0.1425 with 12 responders** to
**0.1625 with 32 responders**.
The larger resource pools therefore extend service reliability, while the marginal benefit of
each additional responder eventually diminishes.

The upper-bound extension closed the bootstrap censoring seen at 24 and 32 responders in the
first confirmatory run. The finite bootstrap fractions are now effectively 1.0 for all frozen
boundary estimates.

### Algorithmic result

Within the fine-grid confirmatory run, Global Minimum-Cost Assignment beat the sequential Greedy
baseline on total response time in all **66 /
66** tested cells after Holm correction. In the
upper-bound extension, the same statement held for all
**36 /
36** cells.

The interpretation remains deliberately narrow: global optimisation improves assignment
efficiency among reachable resources. It does not create road connectivity that is absent from
the disrupted graph.

### Scientific boundary

The severity variable is a **synthetic stress-control parameter**. It is not earthquake magnitude,
PGA, an engineering fragility index, or an official emergency threshold. These results describe
the behaviour of the research model under controlled stochastic road disruption in the Beykoz
pilot network.

---

## Türkçe

### Birincil doğrulayıcı sonuç

Son Beykoz doğrulama analizi, sentetik **80/80 hizmet güvenilirliği sınırını** tahmin eder:
olayların en az %80'ine erişilebilirliğin en az %80 olasılıkla korunabildiği sentetik kesinti
şiddeti sınırı.

| Müdahale ekibi | Sınır tahmini | %95 dünya-bootstrap aralığı |
|---:|---:|---:|
| 12 | 0.142500 | 0.134000–0.148462 |
| 14 | 0.149167 | 0.142500–0.156000 |
| 16 | 0.152500 | 0.145333–0.160000 |
| 20 | 0.154500 | 0.147000–0.163214 |
| 24 | 0.158333 | 0.148462–0.168214 |
| 32 | 0.162500 | 0.154167–0.172727 |

Müdahale ekibi sayısı arttıkça sınır daha yüksek kesinti şiddetlerine taşınmaktadır; ancak kaynak
artışının getirisi doğrusal değildir. 12 ekipte yaklaşık
**0.1425** olan sınır, 32 ekipte yaklaşık
**0.1625** düzeyine yükselmiştir.

Global Minimum-Cost Assignment, erişilebilir kaynakların tahsisinde Greedy yönteme göre müdahale
süresini sistematik biçimde azaltmıştır. Buna karşılık, kopmuş yol bağlantısını yeniden
oluşturamaz; bu nedenle yüksek kesinti düzeylerinde ağ bağlantılılığı temel sınırlayıcı hâline
gelmektedir.

Buradaki şiddet değişkeni **sentetik bir stres kontrolüdür**; deprem büyüklüğü, mühendislik
kırılganlık indeksi veya resmî operasyon eşiği değildir.

---

## Español (España)

### Resultado confirmatorio principal

El análisis confirmatorio final de Beykoz estima la **frontera de fiabilidad 80/80**: el nivel del
control sintético de interrupción en el que la probabilidad de conservar al menos un 80% de
accesibilidad cruza el 80%.

| Recursos de respuesta | Estimación de frontera | Intervalo bootstrap del 95% |
|---:|---:|---:|
| 12 | 0.142500 | 0.134000–0.148462 |
| 14 | 0.149167 | 0.142500–0.156000 |
| 16 | 0.152500 | 0.145333–0.160000 |
| 20 | 0.154500 | 0.147000–0.163214 |
| 24 | 0.158333 | 0.148462–0.168214 |
| 32 | 0.162500 | 0.154167–0.172727 |

La frontera se desplaza hacia niveles de interrupción más altos cuando aumenta la disponibilidad
de recursos, aunque el beneficio marginal no es lineal. La estimación pasa de aproximadamente
**0.1425** con 12 recursos a
**0.1625** con 32.

La Asignación Global de Coste Mínimo reduce de forma sistemática el coste temporal de asignación
frente al método Greedy entre los recursos que siguen siendo alcanzables. No puede recuperar
conectividad viaria inexistente.

La severidad utilizada aquí es un **parámetro sintético de estrés**; no equivale a magnitud
sísmica, PGA, un índice de fragilidad de ingeniería ni un umbral operativo oficial.
