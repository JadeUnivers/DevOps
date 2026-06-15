"""
Airbnb Analytics Platform - Application Streamlit
Basée sur DuckDB + dbt (couche Gold)
"""

import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ─────────────────────────────────────────────────────────
# CONFIG PAGE
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Airbnb Analytics",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────
# CONNEXION DUCKDB
# ─────────────────────────────────────────────────────────
DB_PATH = Path(__file__).parent.parent / "airbnb.duckdb"


@st.cache_resource
def get_connection():
    return duckdb.connect(str(DB_PATH), read_only=True)


@st.cache_data(ttl=300)
def run_query(sql: str) -> pd.DataFrame:
    conn = get_connection()
    return conn.execute(sql).df()


# ─────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/6/69/Airbnb_Logo_B%C3%A9lo.svg",
    width=160,
)
st.sidebar.title("Airbnb Analytics")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "📊 Navigation",
    [
        "🏠 Vue d'ensemble",
        "🛏️ Analyse des logements",
        "👤 Analyse des hôtes",
        "⭐ Analyse des avis",
        "🌕 Impact Pleine Lune",
    ],
)

# ─────────────────────────────────────────────────────────
# PAGE 1 — VUE D'ENSEMBLE
# ─────────────────────────────────────────────────────────
if page == "🏠 Vue d'ensemble":
    st.title("🏠 Airbnb Analytics Platform")
    st.markdown("Bienvenue sur le tableau de bord analytique Airbnb — propulsé par **DuckDB** & **dbt**.")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    nb_listings = run_query("SELECT COUNT(*) AS n FROM gold.dim_listings")["n"][0]
    nb_hosts    = run_query("SELECT COUNT(*) AS n FROM gold.dim_hosts")["n"][0]
    nb_reviews  = run_query("SELECT COUNT(*) AS n FROM gold.fact_reviews")["n"][0]
    nb_super    = run_query("SELECT COUNT(*) AS n FROM gold.dim_hosts WHERE is_superhost = TRUE")["n"][0]

    col1.metric("🏠 Logements", f"{nb_listings:,}")
    col2.metric("👤 Hôtes",     f"{nb_hosts:,}")
    col3.metric("⭐ Avis",      f"{nb_reviews:,}")
    col4.metric("🌟 Superhosts",f"{nb_super:,}")

    st.markdown("---")
    st.subheader("Répartition des sentiments globaux")
    df_sent = run_query("""
        SELECT sentiment, COUNT(*) AS nb
        FROM gold.fact_reviews
        WHERE sentiment IS NOT NULL
        GROUP BY sentiment
        ORDER BY nb DESC
    """)
    color_map = {"positive": "#00C853", "neutral": "#FFC107", "negative": "#F44336"}
    fig = px.pie(df_sent, names="sentiment", values="nb",
                 color="sentiment", color_discrete_map=color_map,
                 hole=0.4)
    fig.update_traces(textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────────────────
# PAGE 2 — LOGEMENTS
# ─────────────────────────────────────────────────────────
elif page == "🛏️ Analyse des logements":
    st.title("🛏️ Analyse des logements")
    st.markdown("---")

    # Filtre type de chambre
    room_types = run_query("SELECT DISTINCT room_type FROM gold.dim_listings WHERE room_type IS NOT NULL ORDER BY 1")["room_type"].tolist()
    selected_rooms = st.multiselect("Filtrer par type de logement", room_types, default=room_types)

    if not selected_rooms:
        st.warning("Sélectionne au moins un type de logement.")
        st.stop()

    rooms_str = ", ".join(f"'{r}'" for r in selected_rooms)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Répartition par type de logement")
        df_type = run_query(f"""
            SELECT room_type, COUNT(*) AS nb_listings
            FROM gold.dim_listings
            WHERE room_type IN ({rooms_str})
            GROUP BY room_type ORDER BY nb_listings DESC
        """)
        fig = px.bar(df_type, x="room_type", y="nb_listings",
                     color="room_type", text="nb_listings")
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Distribution des prix par type")
        df_price = run_query(f"""
            SELECT room_type, price
            FROM gold.dim_listings
            WHERE room_type IN ({rooms_str}) AND price IS NOT NULL AND price > 0
        """)
        fig = px.box(df_price, x="room_type", y="price", color="room_type",
                     points="outliers")
        fig.update_layout(yaxis_title="Prix / nuit ($)")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 10 logements les plus chers")
    df_top = run_query(f"""
        SELECT listing_name, room_type, price, host_name, minimum_nights
        FROM gold.dim_listings
        WHERE room_type IN ({rooms_str}) AND price IS NOT NULL
        ORDER BY price DESC LIMIT 10
    """)
    st.dataframe(df_top, use_container_width=True)

# ─────────────────────────────────────────────────────────
# PAGE 3 — HÔTES
# ─────────────────────────────────────────────────────────
elif page == "👤 Analyse des hôtes":
    st.title("👤 Analyse des hôtes")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Superhosts vs Hôtes standard")
        df_super = run_query("""
            SELECT
                CASE WHEN is_superhost THEN '⭐ Superhost' ELSE 'Hôte standard' END AS statut,
                COUNT(*) AS nb
            FROM gold.dim_hosts
            GROUP BY is_superhost
        """)
        fig = px.pie(df_super, names="statut", values="nb",
                     color_discrete_sequence=["#FF5A5F", "#484848"], hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Prix moyen : Superhost vs Standard")
        df_price_host = run_query("""
            SELECT
                CASE WHEN h.is_superhost THEN '⭐ Superhost' ELSE 'Standard' END AS statut,
                ROUND(AVG(l.price), 2) AS prix_moyen
            FROM gold.dim_listings l
            JOIN gold.dim_hosts h ON l.host_id = h.host_id
            WHERE l.price IS NOT NULL
            GROUP BY h.is_superhost
        """)
        fig = px.bar(df_price_host, x="statut", y="prix_moyen",
                     color="statut", text="prix_moyen",
                     color_discrete_sequence=["#FF5A5F", "#767676"])
        fig.update_traces(texttemplate="%{text:.2f} $", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 10 hôtes par nombre de logements")
    df_top_hosts = run_query("""
        SELECT h.host_name,
               CASE WHEN h.is_superhost THEN '⭐' ELSE '' END AS superhost,
               COUNT(l.listing_id) AS nb_logements,
               ROUND(AVG(l.price), 2) AS prix_moyen
        FROM gold.dim_hosts h
        JOIN gold.dim_listings l ON h.host_id = l.host_id
        GROUP BY h.host_name, h.is_superhost
        ORDER BY nb_logements DESC
        LIMIT 10
    """)
    st.dataframe(df_top_hosts, use_container_width=True)

# ─────────────────────────────────────────────────────────
# PAGE 4 — AVIS
# ─────────────────────────────────────────────────────────
elif page == "⭐ Analyse des avis":
    st.title("⭐ Analyse des avis clients")
    st.markdown("---")

    # Filtre reviewer
    reviewers = run_query("""
        SELECT DISTINCT reviewer_name
        FROM gold.fact_reviews
        WHERE reviewer_name IS NOT NULL
        ORDER BY 1
        LIMIT 200
    """)["reviewer_name"].tolist()

    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        selected_reviewer = st.selectbox("Filtrer par reviewer (optionnel)", ["Tous"] + reviewers)
    with col_f2:
        selected_sentiment = st.selectbox("Filtrer par sentiment", ["Tous", "positive", "neutral", "negative"])

    where_clauses = []
    if selected_reviewer != "Tous":
        where_clauses.append(f"reviewer_name = '{selected_reviewer}'")
    if selected_sentiment != "Tous":
        where_clauses.append(f"sentiment = '{selected_sentiment}'")
    where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribution des sentiments")
        df_sent = run_query(f"""
            SELECT sentiment, COUNT(*) AS nb
            FROM gold.fact_reviews {where_sql}
            GROUP BY sentiment ORDER BY nb DESC
        """)
        color_map = {"positive": "#00C853", "neutral": "#FFC107", "negative": "#F44336"}
        fig = px.bar(df_sent, x="sentiment", y="nb", color="sentiment",
                     color_discrete_map=color_map, text="nb")
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Évolution des avis dans le temps")
        df_time = run_query(f"""
            SELECT DATE_TRUNC('month', review_date) AS mois,
                   sentiment, COUNT(*) AS nb
            FROM gold.fact_reviews {where_sql}
            GROUP BY 1, 2 ORDER BY 1
        """)
        if not df_time.empty:
            fig = px.line(df_time, x="mois", y="nb", color="sentiment",
                          color_discrete_map=color_map)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée pour cette sélection.")

    st.subheader("Derniers avis")
    df_reviews = run_query(f"""
        SELECT review_date, reviewer_name, listing_name, sentiment, review_text
        FROM gold.fact_reviews {where_sql}
        ORDER BY review_date DESC LIMIT 50
    """)
    st.dataframe(df_reviews, use_container_width=True)

# ─────────────────────────────────────────────────────────
# PAGE 5 — PLEINE LUNE
# ─────────────────────────────────────────────────────────
elif page == "🌕 Impact Pleine Lune":
    st.title("🌕 Impact des nuits de pleine lune sur les avis")
    st.markdown(
        "Analyse de l'impact des nuits de pleine lune sur le sentiment des avis clients. "
        "Un avis est tagué **full moon** s'il a été posté le lendemain d'une pleine lune."
    )
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sentiment selon la pleine lune")
        df_moon = run_query("""
            SELECT is_full_moon, sentiment, COUNT(*) AS nb
            FROM gold.full_moon_reviews
            WHERE sentiment IS NOT NULL
            GROUP BY is_full_moon, sentiment
            ORDER BY is_full_moon, nb DESC
        """)
        color_map = {"positive": "#00C853", "neutral": "#FFC107", "negative": "#F44336"}
        fig = px.bar(df_moon, x="is_full_moon", y="nb", color="sentiment",
                     barmode="group", color_discrete_map=color_map,
                     labels={"is_full_moon": "Période", "nb": "Nombre d'avis"})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("% Sentiments positifs : lune vs hors lune")
        df_pct = run_query("""
            SELECT
                is_full_moon,
                ROUND(100.0 * SUM(CASE WHEN sentiment = 'positive' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_positive,
                ROUND(100.0 * SUM(CASE WHEN sentiment = 'negative' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_negative,
                ROUND(100.0 * SUM(CASE WHEN sentiment = 'neutral'  THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_neutral
            FROM gold.full_moon_reviews
            WHERE sentiment IS NOT NULL
            GROUP BY is_full_moon
        """)
        fig = go.Figure()
        for col_name, color in [("pct_positive","#00C853"),("pct_neutral","#FFC107"),("pct_negative","#F44336")]:
            fig.add_trace(go.Bar(
                name=col_name.replace("pct_",""),
                x=df_pct["is_full_moon"],
                y=df_pct[col_name],
                marker_color=color,
                text=df_pct[col_name].astype(str) + "%",
                textposition="auto"
            ))
        fig.update_layout(barmode="stack", yaxis_title="%", xaxis_title="Période")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Statistiques détaillées")
    df_stats = run_query("""
        SELECT
            is_full_moon                    AS période,
            COUNT(*)                        AS total_avis,
            SUM(CASE WHEN sentiment = 'positive' THEN 1 ELSE 0 END) AS positifs,
            SUM(CASE WHEN sentiment = 'negative' THEN 1 ELSE 0 END) AS négatifs,
            SUM(CASE WHEN sentiment = 'neutral'  THEN 1 ELSE 0 END) AS neutres
        FROM gold.full_moon_reviews
        WHERE sentiment IS NOT NULL
        GROUP BY is_full_moon
        ORDER BY is_full_moon
    """)
    st.dataframe(df_stats, use_container_width=True)

    st.info(
        "💡 **Interprétation** : Si le pourcentage d'avis négatifs est plus élevé lors des nuits de pleine lune, "
        "cela pourrait indiquer un impact comportemental lié au cycle lunaire sur l'expérience des voyageurs."
    )
