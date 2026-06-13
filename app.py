import mysql.connector
import pandas as pd
import plotly.express as px
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Rafi Global Football Analytics 2026",
    page_icon="⚽",
    layout="wide",
)

db_config = {
    "host": "localhost",
    "user": "rafi_developer",
    "password": os.getenv("DB_PASSWORD"),
    "database": "db_worldcup_science",
    "port": 3306,
}

def ambil_data_riil():
    try:
        conn = mysql.connector.connect(**db_config)
        query = "SELECT * FROM tabel_pertandingan"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Gagal memuat database riil: {e}")
        return pd.DataFrame()

def ambil_data_akurasi():
    try:
        conn = mysql.connector.connect(**db_config)
        query_join = """
        SELECT 
            p.fase, 
            p.tim_1, 
            p.tim_2, 
            p.prediksi_pemenang,
            CASE 
                WHEN r.skor_home > r.skor_away THEN r.tim_home
                WHEN r.skor_away > r.skor_home THEN r.tim_away
                ELSE 'SERI'
            END as pemenang_asli
        FROM tabel_prediksi_bracket p
        INNER JOIN tabel_pertandingan r 
            ON (p.tim_1 = r.tim_home AND p.tim_2 = r.tim_away)
            OR (p.tim_1 = r.tim_away AND p.tim_2 = r.tim_home)
        """
        df_akurasi = pd.read_sql(query_join, conn)
        conn.close()
        return df_akurasi
    except Exception as e:
        st.error(f"Gagal memuat data evaluasi: {e}")
        return pd.DataFrame()

st.title("⚽ Global Football Tournament 2026 Analytics Platform")
st.caption("Developed by Rafi | Docker MySQL, Python API, and Streamlit Integration")

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Live Tournament Statistics",
        "🎯 Bracket Accuracy Evaluation",
        "🎨 UI/UX Design & Bracket Architecture",
    ]
)

with tab1:
    data_df = ambil_data_riil()

    if not data_df.empty:
        col1, col2, col3 = st.columns(3)

        with col1:
            total_laga = len(data_df)
            st.metric(label="Total Matches Recorded", value=total_laga)

        with col2:
            total_gol = data_df["skor_home"].sum() + data_df["skor_away"].sum()
            st.metric(label="Total Goals Scored", value=int(total_gol))

        with col3:
            rerata_gol = total_gol / total_laga
            st.metric(label="Average Goals / Match", value=f"{rerata_gol:.2f}")

        st.divider()
        st.subheader("📊 Goal Statistics per Team")

        df_home = data_df[["tim_home", "skor_home"]].rename(
            columns={"tim_home": "Tim", "skor_home": "Gol"}
        )
        df_away = data_df[["tim_away", "skor_away"]].rename(
            columns={"tim_away": "Tim", "skor_away": "Gol"}
        )
        df_total_gol = (
            pd.concat([df_home, df_away]).groupby("Tim").sum().reset_index()
        )

        fig = px.bar(
            df_total_gol,
            x="Tim",
            y="Gol",
            title="Total Goals Scored by Each Country",
            color="Gol",
            text_auto=True,
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📋 Live Match Results in Database")
        st.dataframe(data_df, use_container_width=True)

    else:
        st.warning(
            "⚠️ Database is empty or disconnected. Ensure the Docker container is running!"
        )

with tab2:
    st.subheader("🎯 Predictive Model Accuracy Detector")
    st.write(
        "The system automatically evaluates the tournament predictive bracket model against real-world data."
    )

    df_acc = ambil_data_akurasi()

    if not df_acc.empty:
        df_acc["STATUS"] = df_acc.apply(
            lambda row: (
                "✅ SUCCESS"
                if row["prediksi_pemenang"] == row["pemenang_asli"]
                else "❌ MISSED"
            ),
            axis=1,
        )

        total_gugur = len(df_acc)
        benar_gugur = len(df_acc[df_acc["STATUS"] == "✅ SUCCESS"])
        persentase = (benar_gugur / total_gugur) * 100

        col_acc1, col_acc2 = st.columns([1, 2])
        with col_acc1:
            st.metric(label="Knockout Matches Finished", value=total_gugur)
            st.metric(label="Accurate Predictions", value=benar_gugur)
            st.subheader(f"🎯 Accuracy Rate: {persentase:.2f}%")

        with col_acc2:
            fig_pie = px.pie(
                df_acc,
                names="STATUS",
                title="Prediction Results Proportion",
                hole=0.4,
                color="STATUS",
                color_discrete_map={"✅ SUCCESS": "#2ecc71", "❌ MISSED": "#e74c3c"},
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        st.subheader("📊 Real Outcomes vs Predicted Bracket Data")
        st.dataframe(df_acc, use_container_width=True)
    else:
        st.warning(
            "⚠️ Knockout stage matches have not concluded yet. Accuracy will be calculated automatically once the matches begin!"
        )

with tab3:
    st.subheader("🎨 Visual Blueprint Bracket & UI/UX Design")
    st.markdown(
        """
        As part of the platform engineering process, the prediction data is derived and mapped directly 
        from the tournament structural bracket visualization into the Docker MySQL ecosystem.
        """
    )

    st.image(
        "tournament_bracket.png",
        caption="Tournament Knockout Stage Structural Prediction Mapping",
        use_container_width=True,
    )
    
    st.divider()
    st.caption(
        "**Disclaimer:** This project is purely developed for educational, data analysis, and portfolio purposes. "
        "All respective copyrights and trademarks of the tournament names belong to their official owners. "
        "This platform is completely independent and has no official affiliation with any sports federation."
    )