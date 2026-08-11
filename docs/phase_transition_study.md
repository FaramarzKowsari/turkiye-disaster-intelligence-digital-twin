# Severity × Responder Phase-Transition Study — v0.5

## English

Benchmark #1 revealed a useful distinction: Global Minimum-Cost Assignment reduced response-time
costs substantially at lower disruption severity, but it did not materially restore reachability
when the synthetic network approached a collapse regime.

The next research question is therefore:

> At what combinations of network disruption and responder availability does the system move from
> an optimisation-limited regime to a resource- or connectivity-limited regime?

v0.5 introduces a two-dimensional sweep over:

- synthetic disruption severity,
- responder availability.

For every severity/seed pair, the road-failure pattern, incident locations and maximum responder
pool are sampled once. Lower-resource conditions use nested prefixes of that same responder pool.
This common-random-numbers design makes resource-level comparisons less noisy.

The benchmark reports:

- mean reachability,
- probability of falling below a collapse threshold,
- probability of meeting a service target,
- minimum responder frontier for a chosen reliability target,
- marginal reachability gained per added responder,
- reduction in weighted unmet demand,
- paired Greedy-vs-Global bootstrap intervals and permutation tests across the full grid.

The disruption model remains synthetic and is not an engineering road-damage model.

## Türkçe

Benchmark #1 önemli bir ayrım ortaya çıkardı: Küresel Minimum Maliyetli Atama, düşük kesinti
şiddetlerinde müdahale süresi maliyetlerini belirgin biçimde azalttı; ancak sentetik ağ çöküş
bölgesine yaklaştığında erişilebilirliği anlamlı ölçüde geri getiremedi.

Bu nedenle yeni araştırma sorusu şudur:

> Ağ kesintisi ve müdahale ekibi sayısının hangi birleşimlerinde sistem, optimizasyonla sınırlı
> bir rejimden kaynak veya bağlantılılıkla sınırlı bir rejime geçmektedir?

v0.5 iki boyutlu bir tarama ekler:

- sentetik kesinti şiddeti,
- kullanılabilir müdahale ekibi sayısı.

Her şiddet/tohum çifti için yol kesintileri, olay konumları ve maksimum müdahale ekibi havuzu bir
kez örneklenir. Daha düşük kaynak koşulları aynı havuzun iç içe geçmiş ön eklerini kullanır. Bu
ortak rastgele sayılar tasarımı, kaynak düzeyleri arasındaki karşılaştırma gürültüsünü azaltır.

Kesinti modeli sentetiktir; mühendislik amaçlı yol hasarı modeli değildir.

## Español (España)

El Benchmark #1 mostró una distinción útil: la Asignación Global de Coste Mínimo redujo de forma
clara los costes de tiempo de respuesta en niveles bajos de interrupción, pero no recuperó de
forma material la accesibilidad cuando la red sintética se aproximó a un régimen de colapso.

La nueva pregunta de investigación es:

> ¿En qué combinaciones de interrupción de red y disponibilidad de recursos pasa el sistema de un
> régimen limitado por la optimización a otro limitado por los recursos o por la conectividad?

La v0.5 incorpora un barrido bidimensional sobre:

- severidad sintética de interrupción,
- número de recursos de respuesta disponibles.

Para cada pareja severidad/semilla se muestrean una sola vez las interrupciones viarias, los
incidentes y el conjunto máximo de recursos. Las condiciones con menos recursos utilizan
subconjuntos anidados del mismo conjunto, reduciendo el ruido de comparación.

El modelo de interrupción sigue siendo sintético y no constituye un modelo de ingeniería de
daños en carreteras.
