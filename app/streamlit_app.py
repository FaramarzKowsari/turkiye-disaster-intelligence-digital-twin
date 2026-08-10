from __future__ import annotations

from datetime import UTC, datetime, timedelta

import plotly.graph_objects as go
import streamlit as st

from turkiye_disaster_twin.config import ISTANBUL_BOUNDS
from turkiye_disaster_twin.data.afad import fetch_events_frame
from turkiye_disaster_twin.data.osm import (
    facility_points,
    load_drive_graph,
    load_emergency_facilities,
)
from turkiye_disaster_twin.visualization import graph_center, graph_line_coordinates

AVATAR_URL = "https://avatars.githubusercontent.com/u/105053743?v=4&s=512"
REPO_URL = "https://github.com/FaramarzKowsari/turkiye-disaster-intelligence-digital-twin"
PAGES_URL = "https://faramarzkowsari.github.io/turkiye-disaster-intelligence-digital-twin/"

DISTRICTS = {
    "Beykoz": "Beykoz, İstanbul, Türkiye",
    "Üsküdar": "Üsküdar, İstanbul, Türkiye",
    "Kadıköy": "Kadıköy, İstanbul, Türkiye",
    "Fatih": "Fatih, İstanbul, Türkiye",
    "Beşiktaş": "Beşiktaş, İstanbul, Türkiye",
}

COPY = {
    "English": {
        "title": "Türkiye Disaster Intelligence Digital Twin",
        "subtitle": "Live research prototype for post-earthquake decision intelligence.",
        "boundary": (
            "Research prototype only. AFAD markers are catalogue events, not damage reports. "
            "This application does not issue official warnings, predict earthquakes or replace "
            "AFAD, public authorities, emergency services or engineering judgement."
        ),
        "live_tab": "Live Digital Twin",
        "research_tab": "Research Design",
        "author_tab": "About the Author",
        "district": "Pilot district",
        "days": "AFAD lookback (days)",
        "minimum": "Minimum magnitude",
        "build": "Build live twin",
        "loading": "Retrieving AFAD and OpenStreetMap data...",
        "events": "AFAD events",
        "nodes": "Road nodes",
        "edges": "Road edges",
        "facilities": "Emergency facilities",
        "map_title": "Live district road graph + emergency facilities + İstanbul AFAD events",
        "no_events": "No AFAD events matched these filters. The road/facility twin is still shown.",
        "data_note": (
            "Roads and facilities are retrieved from OpenStreetMap. AFAD events use the İstanbul "
            "bounding region. Road damage is not inferred in this stage."
        ),
        "research_heading": "Current research design",
        "research": (
            "Under uncertain post-earthquake road disruption and emergency demand, can graph-aware "
            "resource allocation reduce critical response time and unmet demand compared with "
            "transparent static baselines?"
        ),
        "stage": (
            "v0.1 establishes reproducible live data ingestion and a visible graph twin. The next "
            "scientific gate is calibrated scenario generation, followed by optimisation and only "
            "then GNN/MARL."
        ),
        "author_heading": "About the author",
        "role": "Author · Software Engineer · AI Researcher",
        "bio": (
            "Faramarz Kowsari is an author, Software Engineer and AI researcher based in Istanbul. "
            "He has published more than 80 digital titles on international platforms and develops "
            "open research software, technical web tools and educational content."
        ),
    },
    "Türkçe": {
        "title": "Türkiye Afet Zekâsı Dijital İkizi",
        "subtitle": "Deprem sonrası karar zekâsı için canlı araştırma prototipi.",
        "boundary": (
            "Yalnızca araştırma prototipidir. AFAD işaretleri katalog olaylarıdır; hasar raporu "
            "değildir. Uygulama resmî uyarı yayımlamaz, deprem tahmini yapmaz ve AFAD'ın, kamu "
            "kurumlarının, acil hizmetlerin veya mühendislik değerlendirmelerinin yerini almaz."
        ),
        "live_tab": "Canlı Dijital İkiz",
        "research_tab": "Araştırma Tasarımı",
        "author_tab": "Yazar Hakkında",
        "district": "Pilot ilçe",
        "days": "AFAD geriye dönük süre (gün)",
        "minimum": "Minimum büyüklük",
        "build": "Canlı ikizi oluştur",
        "loading": "AFAD ve OpenStreetMap verileri alınıyor...",
        "events": "AFAD olayları",
        "nodes": "Yol düğümleri",
        "edges": "Yol kenarları",
        "facilities": "Acil durum tesisleri",
        "map_title": "Canlı ilçe yol grafı + acil tesisler + İstanbul AFAD olayları",
        "no_events": "Bu filtrelere uyan AFAD olayı yok. Yol ve tesis dijital ikizi yine gösteriliyor.",
        "data_note": (
            "Yollar ve tesisler OpenStreetMap'den alınır. AFAD olayları İstanbul sınır kutusunda "
            "sorgulanır. Bu aşamada yol hasarı tahmini yapılmaz."
        ),
        "research_heading": "Mevcut araştırma tasarımı",
        "research": (
            "Deprem sonrası yol ağındaki belirsiz kesintiler ve acil yardım talebi altında, graf "
            "tabanlı kaynak tahsisi; şeffaf statik temel yöntemlere kıyasla kritik müdahale "
            "süresini ve karşılanamayan talebi azaltabilir mi?"
        ),
        "stage": (
            "v0.1 tekrar üretilebilir canlı veri alımını ve görünür bir graf dijital ikizini kurar. "
            "Sonraki bilimsel eşik kalibre edilmiş senaryo üretimidir; ardından optimizasyon ve "
            "ancak daha sonra GNN/MARL gelir."
        ),
        "author_heading": "Yazar hakkında",
        "role": "Yazar · Yazılım Mühendisi · Yapay Zekâ Araştırmacısı",
        "bio": (
            "Faramarz Kowsari, İstanbul merkezli bir yazar, Yazılım Mühendisi ve Yapay Zekâ "
            "araştırmacısıdır. Uluslararası platformlarda 80'den fazla dijital eser yayımlamış; "
            "açık araştırma yazılımları, teknik web araçları ve eğitim içerikleri geliştirmektedir."
        ),
    },
    "Español (España)": {
        "title": "Gemelo Digital de Inteligencia ante Desastres de Türkiye",
        "subtitle": "Prototipo de investigación en vivo para inteligencia de decisión tras un terremoto.",
        "boundary": (
            "Prototipo exclusivamente de investigación. Los marcadores de AFAD son eventos de "
            "catálogo, no informes de daños. La aplicación no emite avisos oficiales, no predice "
            "terremotos y no sustituye a AFAD, a las administraciones, a los servicios de "
            "emergencia ni al criterio de ingeniería."
        ),
        "live_tab": "Gemelo Digital en Vivo",
        "research_tab": "Diseño de Investigación",
        "author_tab": "Sobre el Autor",
        "district": "Distrito piloto",
        "days": "Periodo retrospectivo de AFAD (días)",
        "minimum": "Magnitud mínima",
        "build": "Construir gemelo en vivo",
        "loading": "Recuperando datos de AFAD y OpenStreetMap...",
        "events": "Eventos de AFAD",
        "nodes": "Nodos viarios",
        "edges": "Aristas viarias",
        "facilities": "Instalaciones de emergencia",
        "map_title": "Grafo viario + instalaciones de emergencia + eventos AFAD de Estambul",
        "no_events": "Ningún evento AFAD coincide con los filtros. El gemelo viario sigue visible.",
        "data_note": (
            "Las carreteras y las instalaciones proceden de OpenStreetMap. Los eventos AFAD se "
            "consultan para el ámbito de Estambul. En esta fase no se infieren daños en carreteras."
        ),
        "research_heading": "Diseño actual de investigación",
        "research": (
            "Ante interrupciones inciertas de la red viaria y demanda de emergencia tras un "
            "terremoto, ¿puede la asignación de recursos basada en grafos reducir el tiempo crítico "
            "de respuesta y la demanda no atendida frente a métodos base estáticos y transparentes?"
        ),
        "stage": (
            "La v0.1 establece ingestión reproducible de datos en vivo y un gemelo de grafos "
            "visible. El siguiente umbral científico es la generación calibrada de escenarios; "
            "después vendrán la optimización y, solo entonces, GNN/MARL."
        ),
        "author_heading": "Sobre el autor",
        "role": "Autor · Ingeniero de Software · Investigador en Inteligencia Artificial",
        "bio": (
            "Faramarz Kowsari es autor, ingeniero de software e investigador en Inteligencia "
            "Artificial afincado en Estambul. Ha publicado más de 80 títulos digitales en "
            "plataformas internacionales y desarrolla software abierto de investigación, "
            "herramientas técnicas para la web y contenidos educativos."
        ),
    },
}


@st.cache_data(ttl=900, show_spinner=False)
def cached_afad(days: int, minimum_magnitude: float):
    end = datetime.now(UTC)
    start = end - timedelta(days=days)
    return fetch_events_frame(
        start,
        end,
        limit=1000,
        min_lat=ISTANBUL_BOUNDS.min_lat,
        max_lat=ISTANBUL_BOUNDS.max_lat,
        min_lon=ISTANBUL_BOUNDS.min_lon,
        max_lon=ISTANBUL_BOUNDS.max_lon,
        min_magnitude=minimum_magnitude,
    )


@st.cache_resource(show_spinner=False)
def cached_graph(place: str):
    return load_drive_graph(place)


@st.cache_data(ttl=86400, show_spinner=False)
def cached_facilities(place: str):
    return facility_points(load_emergency_facilities(place))


def build_map(graph, facilities, events, title: str):
    lat_center, lon_center = graph_center(graph)
    road_lon, road_lat = graph_line_coordinates(graph)

    figure = go.Figure()
    figure.add_trace(
        go.Scattermap(
            lon=road_lon,
            lat=road_lat,
            mode="lines",
            name="Road network",
            hoverinfo="skip",
            line={"width": 1},
        )
    )

    if not facilities.empty:
        figure.add_trace(
            go.Scattermap(
                lon=facilities["longitude"],
                lat=facilities["latitude"],
                mode="markers",
                name="Emergency facilities",
                text=facilities["name"] + " · " + facilities["category"],
                hoverinfo="text",
                marker={"size": 9},
            )
        )

    if not events.empty:
        sizes = events["magnitude"].fillna(1.0).clip(lower=0.8) * 5
        hover = (
            events["location"].fillna("AFAD event").astype(str)
            + "<br>M "
            + events["magnitude"].fillna(0).round(1).astype(str)
            + "<br>"
            + events["time_utc"].astype(str)
        )
        figure.add_trace(
            go.Scattermap(
                lon=events["longitude"],
                lat=events["latitude"],
                mode="markers",
                name="AFAD earthquakes",
                text=hover,
                hoverinfo="text",
                marker={"size": sizes},
            )
        )

    figure.update_layout(
        title=title,
        map={
            "style": "open-street-map",
            "center": {"lat": lat_center, "lon": lon_center},
            "zoom": 10,
        },
        margin={"l": 0, "r": 0, "t": 45, "b": 0},
        height=680,
        legend={"orientation": "h"},
    )
    return figure


st.set_page_config(
    page_title="Türkiye Disaster Intelligence Digital Twin",
    page_icon="🌐",
    layout="wide",
)

with st.sidebar:
    language = st.selectbox("Language / Dil / Idioma", list(COPY))
    text = COPY[language]
    district_name = st.selectbox(text["district"], list(DISTRICTS))
    lookback_days = st.slider(text["days"], 1, 90, 30)
    minimum_magnitude = st.slider(text["minimum"], 0.0, 6.0, 1.5, 0.1)
    build = st.button(text["build"], width="stretch")
    st.markdown("---")
    st.link_button("GitHub", REPO_URL, width="stretch")
    st.link_button("Project website", PAGES_URL, width="stretch")

text = COPY[language]

st.title(text["title"])
st.caption(text["subtitle"])
st.warning(text["boundary"])

live_tab, research_tab, author_tab = st.tabs(
    [text["live_tab"], text["research_tab"], text["author_tab"]]
)

with live_tab:
    st.caption(text["data_note"])

    if not build:
        st.info(text["build"])
    else:
        place = DISTRICTS[district_name]
        try:
            with st.spinner(text["loading"]):
                events = cached_afad(lookback_days, minimum_magnitude)
                graph = cached_graph(place)
                facilities = cached_facilities(place)

            metrics = st.columns(4)
            metrics[0].metric(text["events"], f"{len(events):,}")
            metrics[1].metric(text["nodes"], f"{graph.number_of_nodes():,}")
            metrics[2].metric(text["edges"], f"{graph.number_of_edges():,}")
            metrics[3].metric(text["facilities"], f"{len(facilities):,}")

            if events.empty:
                st.info(text["no_events"])

            st.plotly_chart(
                build_map(graph, facilities, events, text["map_title"]),
                width="stretch",
            )
        # Public UI boundary: failures can originate from external data services,
        # network transport, parsing, geocoding, Overpass, or graph construction.
        except Exception as exc:  # noqa: BLE001
            st.error(f"Live data retrieval failed: {exc}")
            st.caption(
                "The public app depends on the current availability and rate limits of "
                "AFAD, OpenStreetMap Nominatim and Overpass services."
            )

with research_tab:
    st.subheader(text["research_heading"])
    st.info(text["research"])
    st.write(text["stage"])
    st.markdown(
        """
**v0.1 scientific gate**

- live AFAD ingestion with a stable internal schema
- district-scale OSM road graph
- OSM emergency-facility layer
- reproducible source provenance
- tested graph visualisation helpers
- no road-damage inference yet
"""
    )

with author_tab:
    photo_column, bio_column = st.columns([1, 3])
    with photo_column:
        st.image(AVATAR_URL, caption="Faramarz Kowsari", width=200)
    with bio_column:
        st.subheader(text["author_heading"])
        st.markdown("### Faramarz Kowsari")
        st.markdown(f"**{text['role']}**")
        st.write(text["bio"])
        st.markdown(
            "[ORCID](https://orcid.org/0000-0003-1692-0453) · "
            "[Google Scholar](https://scholar.google.com/citations?user=G7tP5WMAAAAJ&hl=en) · "
            "[GitHub](https://github.com/FaramarzKowsari) · "
            "[LinkedIn](https://www.linkedin.com/in/faramarzkowsari) · "
            "[Official Website](https://faramarzkowsari.github.io)"
        )

st.caption(
    "Türkiye Disaster Intelligence Digital Twin · "
    "Created and maintained by Faramarz Kowsari"
)
