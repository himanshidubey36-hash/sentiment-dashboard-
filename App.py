import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Nifty 50 News Sentiment Analysis Dashboard", layout="wide")

# Load your data
df = pd.read_excel('sentiment_analysis_results.xlsx')
top5 = pd.read_excel('selected_5_companies.xlsx')

# --- SIDEBAR ---
st.sidebar.title("Filters & Controls")

# Interactive: Company selection
all_companies = sorted(df['Company'].unique())
selected_company = st.sidebar.selectbox("Company", all_companies)

# Interactive: Sentiment slider
min_score, max_score = float(df['sentiment'].min()), float(df['sentiment'].max())
score_threshold = st.sidebar.slider("Sentiment Score Threshold", min_value=min_score, max_value=max_score, value=min_score)

# Interactive: Article count display
show_table = st.sidebar.checkbox("Show All Rows of Filtered Table", value=False)

# Filter dataframe based on user selection
filtered_df = df[(df['Company'] == selected_company) & (df['sentiment'] >= score_threshold)]

st.title("📊 Nifty 50 News Sentiment Dashboard")
st.write(f"Use the sidebar on the left to interactively explore sentiment analysis results!")

# --- METRICS ---
col1, col2, col3 = st.columns(3)
col1.metric("Company", selected_company)
col2.metric("Articles Selected", len(filtered_df))
if not filtered_df.empty:
    col3.metric("Average Sentiment", f"{filtered_df['sentiment'].mean():.2f}")
else:
    col3.metric("Average Sentiment", "N/A")

# --- CHART ---
st.subheader(f"Sentiment Scores for {selected_company} (Sentiment≥{score_threshold:.2f})")
if not filtered_df.empty:
    chart = px.bar(filtered_df, x='Published', y='sentiment', color='sentiment',
                   title=f"Sentiment by Date - {selected_company}",
                   color_continuous_scale='RdYlGn')
    st.plotly_chart(chart, use_container_width=True)
else:
    st.info("No articles match current filters.")

# --- TABLE ---
st.subheader("Filtered Article Details")
if not filtered_df.empty:
    # Expand/collapse whole table
    if show_table:
        st.write(filtered_df)
    else:
        st.write(filtered_df.head(10))
    # Download button for filtered data
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(label="⬇️ Download Current Table as CSV", data=csv,
                       file_name=f"{selected_company}_sentiment.csv", mime='text/csv')
else:
    st.warning("No data to display with these filters.")

# --- TOP 5 COMPANIES ---
st.subheader("🏆 Top 5 Companies (Based on Sentiment)")
st.write(top5)

# --- Raw Data Expander ---
with st.expander("Show All Data"):
    st.write(df)

st.caption("Interactive dashboard built with Streamlit • Data from Google News RSS • Sentiment via VADER")
