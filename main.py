import streamlit as st
import pandas as pd
import plotly.express as px

# Page Setup
st.set_page_config(
    page_title="Marriage Rates by Gender",
    layout="wide"
)

st.header("Objective 3: Gender Disaggregated Demographic Marriage Dynamics 💍", divider="gray")

# Load Dataset
try:
    df_marriages = pd.read_csv('marriages_state_CLEANED.csv')
    st.success("Data loaded successfully!")
    st.success("Data loaded successfully!")
    df_marriages['date'] = pd.to_datetime(df_marriages['date'])
    df_marriages['year'] = df_marriages['date'].dt.year

    # State Selector Dropdown
    selected_state = st.selectbox("Select State / Federal Territory:", sorted(df_marriages['state'].unique()), index=11)
    
    state_marr = df_marriages[df_marriages['state'] == selected_state].sort_values('year')

    # Summary Metrics Calculation (2024 data)
    latest_marr = state_marr[state_marr['year'] == 2024]
    
    female_row = latest_marr[latest_marr['sex'] == 'female']
    male_row = latest_marr[latest_marr['sex'] == 'male']
    
    female_rate_2024 = female_row['rate'].values[0] if not female_row.empty else 0.0
    male_rate_2024 = male_row['rate'].values[0] if not male_row.empty else 0.0
    gender_gap = abs(female_rate_2024 - male_rate_2024)
    total_abs_2024 = latest_marr['abs'].sum()

    # 4 Metric Summary Boxes
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Female Marriage Rate (2024)", f"{female_rate_2024:.1f}", help="Female crude marriage rate per 1,000 population", border=True)
    col2.metric("Male Marriage Rate (2024)", f"{male_rate_2024:.1f}", help="Male crude marriage rate per 1,000 population", border=True)
    col3.metric("Gender Rate Gap (2024)", f"{gender_gap:.1f}", help="Absolute difference between female and male marriage rates", border=True)
    col4.metric("Total Marriages (2024)", f"{total_abs_2024:,}", help="Total absolute marriages recorded in 2024", border=True)

    # Raw Data Preview
    st.subheader("Raw Data Preview")
    st.dataframe(state_marr[['state', 'year', 'sex', 'rate', 'abs']])

    # Gender Disaggregated Grouped Line Chart
    st.subheader(f"Gender-Disaggregated Marriage Rate Trends in {selected_state}")

    fig3 = px.line(
        state_marr,
        x='year',
        y='rate',
        color='sex',
        markers=True,
        title=f'Marriage Rate Trajectory by Gender in {selected_state} (2019 - 2024)',
        labels={'year': 'Year', 'rate': 'Marriage Rate (per 1,000 population)', 'sex': 'Gender'},
        color_discrete_map={'female': '#e377c2', 'male': '#1f77b4'}
    )
    fig3.update_xaxes(type='category')
    fig3.update_layout(
        hovermode='x unified',
        legend_title_text='Gender',
        height=450
    )
    fig3.update_traces(line=dict(width=3), marker=dict(size=8))

    st.plotly_chart(fig3, use_container_width=True)

    # Interpretation Section
    st.markdown("### 💬 Scientific Interpretation & Discussion")
    st.info(f"""
    * **Demographic Divergence:** In **{selected_state}**, female and male marriage rates show parallel temporal trends from 2019 to 2024, responding to overarching macro-economic and social shifts.
    * **Rate Discrepancy:** The variance between male and female crude marriage rates is primarily driven by age group distributions and differing median age thresholds at first marriage between genders.
    * **Socioeconomic Impact:** Shifts in marriage rates reflect broader demographic changes, including higher educational attainment, increased career participation among women, and shifting socio-cultural expectations regarding family planning.
    """)

except Exception as e:
    st.error(f"Error loading or processing data: {e}")
