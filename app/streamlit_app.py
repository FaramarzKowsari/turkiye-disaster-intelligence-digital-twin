from __future__ import annotations

import streamlit as st

AVATAR_URL = "https://avatars.githubusercontent.com/u/105053743?v=4&s=512"
REPO_URL = "https://github.com/FaramarzKowsari/turkiye-disaster-intelligence-digital-twin"
PAGES_URL = "https://faramarzkowsari.github.io/turkiye-disaster-intelligence-digital-twin/"

COPY = {
    "English": {
        "title": "Türkiye Disaster Intelligence Digital Twin",
        "subtitle": (
            "Research-grade AI and geospatial decision-support testbed for "
            "post-earthquake emergency response."
        ),
        "boundary": (
            "Research prototype only. This application does not issue official warnings, "
            "predict earthquakes or replace AFAD, public authorities, emergency services "
            "or engineering judgement."
        ),
        "research_kicker": "Research question",
        "research": (
            "Under uncertain post-earthquake road disruption and emergency demand, can "
            "graph-aware resource allocation reduce critical response time and unmet "
            "demand compared with transparent static baselines?"
        ),
        "stage": "Current research stage",
        "stage_text": (
            "v0.1 focuses on reproducible AFAD/OSM ingestion, synthetic disruption scenarios, "
            "transparent baselines, testing and provenance. Optimisation, GNN and MARL are "
            "introduced only after the baseline simulator is stable."
        ),
        "author_heading": "About the author",
        "role": "Author · Software Engineer · AI Researcher",
        "bio": (
            "Faramarz Kowsari is an author, Software Engineer and AI researcher based in "
            "Istanbul. He has published more than 80 digital titles on international "
            "platforms and develops open research software, technical web tools and "
            "educational content."
        ),
        "source": "Open GitHub source repository",
        "website": "Open project website",
        "metrics": ["Response time", "Unmet demand", "Reachability", "Fairness"],
    },
    "Türkçe": {
        "title": "Türkiye Afet Zekâsı Dijital İkizi",
        "subtitle": (
            "Deprem sonrası acil müdahale için araştırma düzeyinde yapay zekâ ve "
            "mekânsal karar destek test ortamı."
        ),
        "boundary": (
            "Yalnızca araştırma prototipidir. Bu uygulama resmî uyarı yayımlamaz, deprem "
            "tahmini yapmaz ve AFAD'ın, kamu kurumlarının, acil hizmetlerin veya mühendislik "
            "değerlendirmelerinin yerini almaz."
        ),
        "research_kicker": "Araştırma sorusu",
        "research": (
            "Deprem sonrası yol ağındaki belirsiz kesintiler ve acil yardım talebi altında, "
            "graf tabanlı kaynak tahsisi; şeffaf statik temel yöntemlere kıyasla kritik "
            "müdahale süresini ve karşılanamayan talebi azaltabilir mi?"
        ),
        "stage": "Mevcut araştırma aşaması",
        "stage_text": (
            "v0.1; tekrar üretilebilir AFAD/OSM veri alımına, sentetik kesinti senaryolarına, "
            "şeffaf temel yöntemlere, testlere ve veri izlenebilirliğine odaklanır. "
            "Optimizasyon, GNN ve MARL ancak temel simülatör kararlı hâle geldikten sonra eklenir."
        ),
        "author_heading": "Yazar hakkında",
        "role": "Yazar · Yazılım Mühendisi · Yapay Zekâ Araştırmacısı",
        "bio": (
            "Faramarz Kowsari, İstanbul merkezli bir yazar, Yazılım Mühendisi ve Yapay Zekâ "
            "araştırmacısıdır. Uluslararası platformlarda 80'den fazla dijital eser "
            "yayımlamış; açık araştırma yazılımları, teknik web araçları ve eğitim "
            "içerikleri geliştirmektedir."
        ),
        "source": "GitHub kaynak kodunu aç",
        "website": "Proje web sitesini aç",
        "metrics": ["Müdahale süresi", "Karşılanamayan talep", "Erişilebilirlik", "Adalet"],
    },
    "Español (España)": {
        "title": "Gemelo Digital de Inteligencia ante Desastres de Türkiye",
        "subtitle": (
            "Entorno de investigación de IA y análisis geoespacial para apoyar la "
            "respuesta de emergencia tras un terremoto."
        ),
        "boundary": (
            "Prototipo exclusivamente de investigación. Esta aplicación no emite avisos "
            "oficiales, no predice terremotos y no sustituye a AFAD, a las administraciones "
            "públicas, a los servicios de emergencia ni al criterio de ingeniería."
        ),
        "research_kicker": "Pregunta de investigación",
        "research": (
            "Ante interrupciones inciertas de la red viaria y demanda de emergencia tras "
            "un terremoto, ¿puede la asignación de recursos basada en grafos reducir el "
            "tiempo crítico de respuesta y la demanda no atendida frente a métodos base "
            "estáticos y transparentes?"
        ),
        "stage": "Fase actual de investigación",
        "stage_text": (
            "La versión v0.1 se centra en la ingestión reproducible de AFAD/OSM, escenarios "
            "sintéticos de interrupción, métodos base transparentes, pruebas y procedencia "
            "de los datos. La optimización, las GNN y MARL se incorporarán cuando el "
            "simulador base sea estable."
        ),
        "author_heading": "Sobre el autor",
        "role": "Autor · Ingeniero de Software · Investigador en Inteligencia Artificial",
        "bio": (
            "Faramarz Kowsari es autor, ingeniero de software e investigador en Inteligencia "
            "Artificial afincado en Estambul. Ha publicado más de 80 títulos digitales en "
            "plataformas internacionales y desarrolla software abierto de investigación, "
            "herramientas técnicas para la web y contenidos educativos."
        ),
        "source": "Abrir el repositorio en GitHub",
        "website": "Abrir el sitio web del proyecto",
        "metrics": ["Tiempo de respuesta", "Demanda no atendida", "Accesibilidad", "Equidad"],
    },
}

st.set_page_config(
    page_title="Türkiye Disaster Intelligence Digital Twin",
    page_icon="🌐",
    layout="wide",
)

with st.sidebar:
    language = st.selectbox("Language / Dil / Idioma", list(COPY))
    st.markdown("---")
    st.link_button("GitHub", REPO_URL, width="stretch")
    st.link_button("Project website", PAGES_URL, width="stretch")

text = COPY[language]

st.title(text["title"])
st.caption(text["subtitle"])
st.warning(text["boundary"])

st.markdown(f"### {text['research_kicker']}")
st.info(text["research"])

st.markdown(f"### {text['stage']}")
st.write(text["stage_text"])

metric_columns = st.columns(4)
for column, label in zip(metric_columns, text["metrics"], strict=True):
    column.metric(label, "Baseline")

st.divider()

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

st.divider()
buttons = st.columns(2)
buttons[0].link_button(text["source"], REPO_URL, width="stretch")
buttons[1].link_button(text["website"], PAGES_URL, width="stretch")

st.caption(
    "Türkiye Disaster Intelligence Digital Twin · "
    "Created and maintained by Faramarz Kowsari"
)
