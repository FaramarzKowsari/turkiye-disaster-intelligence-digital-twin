<p align="center">
  <img src="https://avatars.githubusercontent.com/u/105053743?v=4&s=512" width="138" height="138" alt="Faramarz Kowsari">
</p>

<h1 align="center">Türkiye Disaster Intelligence Digital Twin</h1>

<p align="center">
  <strong>Research-grade AI and geospatial decision-support testbed for earthquake response in İstanbul, designed to scale across Türkiye.</strong>
</p>

<p align="center">
  <a href="https://github.com/FaramarzKowsari/turkiye-disaster-intelligence-digital-twin/actions/workflows/ci.yml">
    <img alt="CI" src="https://github.com/FaramarzKowsari/turkiye-disaster-intelligence-digital-twin/actions/workflows/ci.yml/badge.svg">
  </a>
  <img alt="Python 3.11+" src="https://img.shields.io/badge/Python-3.11%2B-3670A0.svg">
  <img alt="License MIT" src="https://img.shields.io/badge/License-MIT-168D73.svg">
  <img alt="Research prototype" src="https://img.shields.io/badge/Status-Research%20Prototype-F3B43F.svg">
  <img alt="No paid AI API required" src="https://img.shields.io/badge/Paid%20AI%20API-Not%20Required-168D73.svg">
</p>

<p align="center">
  <a href="#english">English</a> ·
  <a href="#türkçe">Türkçe</a> ·
  <a href="#español-españa">Español (España)</a> ·
  <a href="https://faramarzkowsari.github.io/turkiye-disaster-intelligence-digital-twin/">Project Website</a>
</p>

> **Research and safety boundary:** this repository is a research prototype. It does not issue
> official warnings, predict earthquakes, estimate certified casualties or losses, or replace
> AFAD, public authorities, emergency-management organisations, hospitals or engineering judgement.

---

<a id="english"></a>

## English

### Research question

> Under uncertain post-earthquake road disruption and emergency demand, can graph-aware resource
> allocation reduce critical response time and unmet demand compared with transparent static
> baselines?

The project models İstanbul as a dynamic emergency-response graph. Earthquake observations,
road accessibility, emergency facilities, incident demand and limited response resources are
combined into reproducible scenarios. The long-term research path moves from transparent
baselines to robust optimisation, Graph Neural Networks and Multi-Agent Reinforcement Learning.

### Research architecture

```text
AFAD earthquake events ─────┐
OpenStreetMap roads ─────────┤
Emergency facilities ────────┼──> Scenario + provenance layer
Future public datasets ──────┘              │
                                            ▼
                                 Dynamic transport graph
                                            │
                  ┌─────────────────────────┼─────────────────────────┐
                  ▼                         ▼                         ▼
             Greedy baselines        Graph optimisation          MARL / GNN
                  └─────────────────────────┼─────────────────────────┘
                                            ▼
                              Response + resilience metrics
```


### Live Digital Twin — v0.1

The public application can build a district-scale İstanbul digital twin on demand using:

- live AFAD earthquake catalogue events within the İstanbul bounding region,
- OpenStreetMap drivable road networks,
- OpenStreetMap hospitals, clinics and fire stations,
- an interactive MapLibre/Plotly map,
- reproducible internal event normalisation.

The first public deployment deliberately uses **district-scale road graphs** to keep live
OpenStreetMap queries responsive. A city-wide İstanbul graph will later be preprocessed,
versioned and served as a cached research artifact.

No paid AI API key is required. At this stage, the map does **not** infer real road damage,
building collapse, casualties or official resource availability.

### Core metrics

- mean, median and p90 response time
- weighted unmet demand
- reachable incident fraction
- hospital overload
- total dispatch travel time
- district fairness gap
- network resilience ratio

### Roadmap

- **v0.1:** reproducible AFAD/OSM ingestion, synthetic disruption scenarios, tested baselines
- **v0.2:** spatial hazard and vulnerability layers, Monte Carlo uncertainty
- **v0.3:** capacitated and multi-objective optimisation
- **v0.4:** PPO/MAPPO Multi-Agent Reinforcement Learning
- **v0.5:** FastAPI/PostGIS-backed interactive digital twin
- **v1.0:** benchmark, ablation studies, reproducibility package and paper-grade release

### About the author

<table>
<tr>
<td width="180" valign="top">
  <img src="https://avatars.githubusercontent.com/u/105053743?v=4&s=512" width="150" alt="Faramarz Kowsari">
</td>
<td valign="top">

#### Faramarz Kowsari

**Author · Software Engineer · AI Researcher**

Faramarz Kowsari is an author, Software Engineer and AI researcher based in Istanbul.
He has published more than 80 digital titles on international platforms and develops
open research software, web-based technical tools and educational content.

This project reflects his current focus on applied artificial intelligence, data-driven
decision support, reproducible research software and public-interest technology.

[ORCID](https://orcid.org/0000-0003-1692-0453) ·
[Google Scholar](https://scholar.google.com/citations?user=G7tP5WMAAAAJ&hl=en) ·
[GitHub](https://github.com/FaramarzKowsari) ·
[LinkedIn](https://www.linkedin.com/in/faramarzkowsari) ·
[Official Website](https://faramarzkowsari.github.io) ·
[Zenodo](https://zenodo.org/search?q=creators.orcid%3A%220000-0003-1692-0453%22)

</td>
</tr>
</table>

---

<a id="türkçe"></a>

## Türkçe

### Araştırma sorusu

> Deprem sonrası yol ağındaki belirsiz kesintiler ve acil yardım talebi altında, graf tabanlı
> kaynak tahsisi; şeffaf ve statik temel yöntemlere kıyasla kritik müdahale süresini ve
> karşılanamayan talebi azaltabilir mi?

Proje, İstanbul'u dinamik bir acil müdahale grafı olarak modeller. Deprem gözlemleri, yol
erişilebilirliği, acil yardım tesisleri, olay talebi ve sınırlı müdahale kaynakları tekrar
üretilebilir senaryolarda bir araya getirilir. Araştırma yol haritası; açıklanabilir temel
yöntemlerden sağlam optimizasyona, Graf Sinir Ağlarına ve Çok Etmenli Pekiştirmeli Öğrenmeye ilerler.


### Canlı Dijital İkiz — v0.1

Halka açık uygulama, isteğe bağlı olarak ilçe ölçeğinde bir İstanbul dijital ikizi oluşturabilir:

- İstanbul coğrafi sınırındaki canlı AFAD deprem katalog olayları,
- OpenStreetMap sürüş yolu ağı,
- OpenStreetMap hastane, klinik ve itfaiye tesisleri,
- etkileşimli MapLibre/Plotly haritası,
- tekrar üretilebilir dahili olay normalizasyonu.

İlk halka açık sürüm, canlı OpenStreetMap sorgularını hızlı ve kararlı tutmak için bilinçli olarak
**ilçe ölçeğinde yol grafı** kullanır. İstanbul'un tamamını kapsayan ağ daha sonra önceden işlenecek,
sürümlenecek ve önbelleğe alınmış bir araştırma çıktısı olarak sunulacaktır.

Ücretli bir yapay zekâ API anahtarı gerekmez. Bu aşamada harita gerçek yol hasarı, bina çökmesi,
can kaybı veya resmî kaynak mevcudiyeti tahmini yapmaz.

### Temel ölçütler

- ortalama, medyan ve p90 müdahale süresi
- ağırlıklı karşılanamayan talep
- erişilebilir olay oranı
- hastane aşırı yükü
- toplam müdahale seyahat süresi
- ilçeler arası adalet farkı
- ağ dayanıklılık oranı

### Yol haritası

- **v0.1:** tekrar üretilebilir AFAD/OSM veri alımı, sentetik kesinti senaryoları ve test edilmiş temel yöntemler
- **v0.2:** mekânsal tehlike ve kırılganlık katmanları, Monte Carlo belirsizlik analizi
- **v0.3:** kapasiteli ve çok amaçlı optimizasyon
- **v0.4:** PPO/MAPPO tabanlı Çok Etmenli Pekiştirmeli Öğrenme
- **v0.5:** FastAPI/PostGIS destekli etkileşimli dijital ikiz
- **v1.0:** benchmark, ablation çalışmaları, tekrar üretilebilirlik paketi ve makale düzeyinde sürüm

### Yazar hakkında

<table>
<tr>
<td width="180" valign="top">
  <img src="https://avatars.githubusercontent.com/u/105053743?v=4&s=512" width="150" alt="Faramarz Kowsari">
</td>
<td valign="top">

#### Faramarz Kowsari

**Yazar · Yazılım Mühendisi · Yapay Zekâ Araştırmacısı**

Faramarz Kowsari, İstanbul merkezli bir yazar, Yazılım Mühendisi ve Yapay Zekâ araştırmacısıdır.
Uluslararası platformlarda 80'den fazla dijital eser yayımlamış; açık araştırma yazılımları,
web tabanlı teknik araçlar ve eğitim içerikleri geliştirmektedir.

Bu proje; uygulamalı yapay zekâ, veriye dayalı karar desteği, tekrar üretilebilir araştırma
yazılımı ve kamu yararına teknoloji çalışmalarına odaklanan güncel araştırma yönünü yansıtır.

[ORCID](https://orcid.org/0000-0003-1692-0453) ·
[Google Scholar](https://scholar.google.com/citations?user=G7tP5WMAAAAJ&hl=en) ·
[GitHub](https://github.com/FaramarzKowsari) ·
[LinkedIn](https://www.linkedin.com/in/faramarzkowsari) ·
[Resmî Web Sitesi](https://faramarzkowsari.github.io) ·
[Zenodo](https://zenodo.org/search?q=creators.orcid%3A%220000-0003-1692-0453%22)

</td>
</tr>
</table>

---

<a id="español-españa"></a>

## Español (España)

### Pregunta de investigación

> Ante interrupciones inciertas de la red viaria y una demanda de emergencia posterior a un
> terremoto, ¿puede una asignación de recursos basada en grafos reducir el tiempo crítico de
> respuesta y la demanda no atendida frente a métodos de referencia estáticos y transparentes?

El proyecto modela Estambul como un grafo dinámico de respuesta a emergencias. Las observaciones
sísmicas, la accesibilidad viaria, las instalaciones de emergencia, la demanda de incidentes y
los recursos limitados se integran en escenarios reproducibles. La línea de investigación
avanza desde métodos de referencia interpretables hacia optimización robusta, Redes Neuronales
de Grafos y Aprendizaje por Refuerzo Multiagente.


### Gemelo Digital en Vivo — v0.1

La aplicación pública puede construir bajo demanda un gemelo digital de Estambul a escala de
distrito utilizando:

- eventos del catálogo sísmico de AFAD para el ámbito geográfico de Estambul,
- redes viarias transitables de OpenStreetMap,
- hospitales, clínicas y parques de bomberos de OpenStreetMap,
- un mapa interactivo con MapLibre/Plotly,
- normalización reproducible de los eventos en un esquema interno estable.

La primera versión pública utiliza deliberadamente **grafos viarios a escala de distrito** para
mantener ágiles y estables las consultas en vivo a OpenStreetMap. Más adelante se preprocesará,
versionará y almacenará en caché un grafo que abarque todo Estambul.

No se necesita ninguna clave de API de IA de pago. En esta fase, el mapa no infiere daños reales
en carreteras, derrumbes de edificios, víctimas ni disponibilidad oficial de recursos.

### Métricas principales

- tiempo de respuesta medio, mediano y percentil 90
- demanda ponderada no atendida
- porcentaje de incidentes alcanzables
- sobrecarga hospitalaria
- tiempo total de desplazamiento de los recursos
- brecha de equidad entre distritos
- índice de resiliencia de la red

### Hoja de ruta

- **v0.1:** ingestión reproducible de AFAD/OSM, escenarios sintéticos de interrupción y métodos base probados
- **v0.2:** capas espaciales de amenaza y vulnerabilidad, incertidumbre mediante Monte Carlo
- **v0.3:** optimización con capacidad y múltiples objetivos
- **v0.4:** Aprendizaje por Refuerzo Multiagente con PPO/MAPPO
- **v0.5:** gemelo digital interactivo respaldado por FastAPI y PostGIS
- **v1.0:** benchmark, estudios de ablación, paquete de reproducibilidad y versión preparada para publicación

### Sobre el autor

<table>
<tr>
<td width="180" valign="top">
  <img src="https://avatars.githubusercontent.com/u/105053743?v=4&s=512" width="150" alt="Faramarz Kowsari">
</td>
<td valign="top">

#### Faramarz Kowsari

**Autor · Ingeniero de Software · Investigador en Inteligencia Artificial**

Faramarz Kowsari es autor, ingeniero de software e investigador en Inteligencia Artificial
afincado en Estambul. Ha publicado más de 80 títulos digitales en plataformas internacionales
y desarrolla software abierto de investigación, herramientas técnicas para la web y contenidos educativos.

Este proyecto refleja su línea actual de trabajo en inteligencia artificial aplicada,
apoyo a la decisión basado en datos, software científico reproducible y tecnología de interés público.

[ORCID](https://orcid.org/0000-0003-1692-0453) ·
[Google Scholar](https://scholar.google.com/citations?user=G7tP5WMAAAAJ&hl=en) ·
[GitHub](https://github.com/FaramarzKowsari) ·
[LinkedIn](https://www.linkedin.com/in/faramarzkowsari) ·
[Sitio web oficial](https://faramarzkowsari.github.io) ·
[Zenodo](https://zenodo.org/search?q=creators.orcid%3A%220000-0003-1692-0453%22)

</td>
</tr>
</table>

---

## Data principles / Veri ilkeleri / Principios de datos

The project prioritises official or open public sources, reproducible pipelines, explicit
provenance, responsible uncertainty reporting and no dependency on paid AI APIs.

Initial sources:

- AFAD Earthquake Event Service
- OpenStreetMap
- Türkiye Ministry of Health Open Data
- Türkiye National Smart Cities Open Data Platform

## Quick start

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install -e ".[dev]"
pytest -q
ruff check .
```

## Public interfaces

- **Source:** https://github.com/FaramarzKowsari/turkiye-disaster-intelligence-digital-twin
- **Project website:** https://faramarzkowsari.github.io/turkiye-disaster-intelligence-digital-twin/

The interactive deployment will be linked here after the first public deployment is created.

## Citation

```text
Kowsari, F. (2026). Türkiye Disaster Intelligence Digital Twin.
Open-source research software.
```

## Licence

MIT
