import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="Nifty 50 Sentiment Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Nifty 50 News Sentiment Analysis Dashboard")
st.markdown("---")

@st.cache_data
def load_data():
    try:
        df = pd.read_excel('sentiment_analysis_results.xlsx')
        top5 = pd.read_excel('selected_5_companies.xlsx')
        return df, top5
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame()

df, top5 = load_data()

if not df.empty and 'Company' in df.columns and 'sentiment' in df.columns:
    # --- Sidebar interactive filters ---
    st.sidebar.header("Interactive Filters")
    companies = df['Company'].unique()
    selected_company = st.sidebar.selectbox("Select Company", companies)
    sentiment_min = st.sidebar.slider(
        "Minimum Sentiment Score",
        min_value=float(df['sentiment'].min()),
        max_value=float(df['sentiment'].max()),
        value=float(df['sentiment'].min()),
        step=0.01
    )

    filtered_df = df[(df['Company'] == selected_company) & (df['sentiment'] >= sentiment_min)]

    # --- Metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("📰 Filtered Articles", len(filtered_df))
    col2.metric("✅ Positive Articles", (filtered_df['sentiment'] > 0.05).sum())
    avg_sent = filtered_df['sentiment'].mean() if not filtered_df.empty else 0
    col3.metric("📈 Average Sentiment", f"{avg_sent:.3f}")

    # --- Sentiment over time chart ---
    st.header(f"Sentiment Details for {selected_company} (Sentiment ≥ {sentiment_min})")
    if not filtered_df.empty:
        fig = px.bar(
            filtered_df,
            x="Company",
            y="sentiment",
            color="sentiment",
            color_continuous_scale="RdYlGn",
            title=f"Sentiment Over Time for {selected_company}",
            labels={"sentiment": "Sentiment Score"},
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No articles match your filters.")

    # --- Data table + download ---
    st.subheader("Filtered Article Data")
    st.dataframe(filtered_df, use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv,
        file_name=f"{selected_company}_sentiment.csv",
        mime="text/csv"
    )

    st.markdown("---")

    # --- Top 5 companies section ---
    st.subheader("🏆 Top 5 Companies Selected for Analysis")
    if not top5.empty:
        st.dataframe(top5, use_container_width=True, hide_index=True)
        st.info("💡 These companies were selected based on positive sentiment scores and news coverage.")
    else:
        st.warning("Top 5 companies data not available.")

    # --- Expandable raw data section ---
    with st.expander("📰 View All Articles (Full Data)"):
        st.dataframe(df, use_container_width=True)

else:
    st.error("❌ Required data not found or columns missing.")
    st.info("Please ensure the Excel files contain 'Company' and 'sentiment' columns.")

st.markdown("---")
st.caption("Built with Streamlit • Data from Google News RSS • Sentiment Analysis using VADER")
