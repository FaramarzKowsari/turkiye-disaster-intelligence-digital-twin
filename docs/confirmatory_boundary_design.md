# Confirmatory Reliability Boundary Study — v0.7

## English

v0.6 established a monotone, coupled experimental design and located the service-reliability
transition between synthetic severity 0.15 and 0.16 for the tested Beykoz road network. The v0.7
study is deliberately narrower and more statistically intensive.

The confirmatory grid is:

- severities: 0.130, 0.135, 0.140, 0.145, 0.150, 0.1525, 0.155, 0.1575, 0.160, 0.1625, 0.165
- responders: 12, 14, 16, 20, 24, 32
- default worlds: 300
- incidents per world: 10
- independent base seed: 7070

The primary estimand is the synthetic severity at which the probability of maintaining at least
80% reachability falls through 80%. This is a reliability boundary, not an earthquake-magnitude
threshold and not an engineering fragility limit.

### Boundary estimator

For each algorithm and responder count:

1. each stochastic world remains coupled across all severity values;
2. service is defined as reachability >= 80%;
3. empirical service probability is estimated at every tested severity;
4. a weighted pooled-adjacent-violators fit enforces a non-increasing probability curve;
5. the 80% reliability crossing is linearly interpolated between adjacent tested severities;
6. a cluster bootstrap resamples whole stochastic worlds and reports a 95% interval.

The artifact also reports Wilson intervals at every tested severity and a monotonicity audit.

## Türkçe

v0.6, eşleştirilmiş ve monoton deney tasarımını doğruladı ve Beykoz için sentetik hizmet
güvenilirliği geçişinin 0.15 ile 0.16 arasında bulunduğunu gösterdi. v0.7 daha dar bir şiddet
aralığında, daha fazla rastgele dünya ile doğrulayıcı bir çalışma yapar.

Ana ölçüt, en az %80 erişilebilirliğin en az %80 olasılıkla korunabildiği sentetik şiddet sınırıdır.
Bu değer deprem büyüklüğü, mühendislik hasar eşiği veya operasyonel güvenlik limiti değildir.

Her müdahale kaynağı düzeyi için bütün şiddetler aynı rastgele dünyayı paylaşır. Hizmet olasılığı
monoton PAVA ile tahmin edilir; 80/80 geçişi komşu şiddetler arasında enterpole edilir ve bütün
rastgele dünyalar küme olarak yeniden örneklenerek bootstrap güven aralığı hesaplanır.

## Español (España)

La v0.6 confirmó un diseño experimental acoplado y monótono y situó la transición de fiabilidad
del servicio entre las severidades sintéticas 0,15 y 0,16 para la red estudiada de Beykoz. La v0.7
reduce deliberadamente el intervalo de severidad y aumenta el número de mundos estocásticos.

El parámetro principal es la severidad sintética en la que la probabilidad de conservar al menos
un 80% de accesibilidad cruza el 80%. No representa una magnitud sísmica, un umbral de daño de
ingeniería ni un límite operativo real.

La curva de probabilidad se ajusta con PAVA monótono, el cruce 80/80 se interpola entre severidades
adyacentes y el intervalo de incertidumbre se estima mediante bootstrap por mundos completos.
