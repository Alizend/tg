import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Gift Drop Analyzer", layout="wide")

st.title("🎁 Telegram Gift Tracker & Black Background Analyzer")

st.markdown("""
Загрузи CSV-файл с двумя колонками:
- `id` — порядковый номер подарка.
- `is_black` — `1` если подарок с чёрным фоном, `0` если обычный.
""")

uploaded_file = st.file_uploader("Загрузите CSV-файл", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    if "id" not in df.columns or "is_black" not in df.columns:
        st.error("CSV должен содержать колонки 'id' и 'is_black'")
    else:
        df = df.sort_values("id")
        black_ids = df[df["is_black"] == 1]["id"].values

        st.subheader("📊 Статистика")
        st.write(f"Всего записей: {len(df)}")
        st.write(f"С чёрным фоном: {len(black_ids)}")
        
        if len(black_ids) > 1:
            diffs = [j - i for i, j in zip(black_ids[:-1], black_ids[1:])]
            avg_diff = sum(diffs)/len(diffs)
            st.write(f"Среднее расстояние между чёрными фонами: **{avg_diff:.2f}**")
            st.write(f"Минимальные интервалы: {sorted(diffs)[:10]}")

        st.subheader("📈 График появления чёрных фонов")
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.scatter(black_ids, [1]*len(black_ids), color='black', label='Black Background', marker='|', s=200)
        ax.set_xlabel("ID подарка")
        ax.set_yticks([])
        ax.grid(True)
        ax.set_title("Распределение подарков с чёрным фоном")
        st.pyplot(fig)
