import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(
    page_title="India Population Dashboard",
    page_icon="🇮🌏",
    layout="wide"
)
st.markdown("""
<style>
/* background */
.stApp {
    background-color: #EEF2FF !important;
}

/* top header bar */
[data-testid="stHeader"] {
    background-color: #EEF2FF !important;
}

/* sidebar */
section[data-testid="stSidebar"] > div {
    background-color: #4A5568 !important;
}

/* sidebar text white */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* headings black */
h1, h2, h3 {
    color: #000000 !important;
}

/* all text black */
p, div, span, label, li {
    color: #000000 !important;
}

/* metric cards */
[data-testid="stMetric"] {
    background-color: #ffffff !important;
    border: 1px solid #CBD5E0 !important;
    border-radius: 10px !important;
    padding: 15px !important;
}

[data-testid="stMetricValue"] {
    color: #000000 !important;
}

[data-testid="stMetricLabel"] {
    color: #000000 !important;
}

/* fix selectbox */
[data-testid="stSelectbox"] * {
    color: #000000 !important;
    background-color: #ffffff !important;
}

/* fix multiselect */
[data-testid="stMultiSelect"] * {
    color: #000000 !important;
    background-color: #ffffff !important;
}

/* fix dropdown options */
[data-baseweb="select"] * {
    color: #000000 !important;
    background-color: #ffffff !important;
}

/* fix dropdown menu that opens */
[data-baseweb="popover"] * {
    color: #000000 !important;
    background-color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)
page = st.sidebar.radio("Choose Section", 
                        ["🏠 Home", 
                         "📊 State Analysis", 
                         "🏙️ District Analysis"]) 
            
df = pd.read_csv("census2011.csv")
df["Population"] = (df["Population"].astype(str).str.replace(",", "", regex=True))
df["Population"] = pd.to_numeric(df["Population"],errors="coerce")
df["Growth"] = ( df["Growth"].astype(str).str.replace("%", "", regex=True))
df["Growth"] = pd.to_numeric(df["Growth"])
if page == "🏠 Home":
    st.title("🌏 India Population Dashboard")
    st.divider()
    st.write("Welcome to the India Population Dashboard. This dashboard provides a detailed look at population distribution, literacy rates, sex ratio and growth across 640 districts and 28 states of India. Whether you are exploring a specific state or drilling down into a district, this dashboard gives you the data you need in a simple and visual way. Use the sidebar on the left to get started.")
    col1, col2 , col3 = st.columns(3)
    col1.metric("Total Districts", len(df))
    col2.metric("Total States", df["State"].nunique())
    col3.metric("Total Population", f"{df['Population'].sum():,}")
    st.subheader("Top 5 Most Populated States")
    state_pop = df.groupby("State")["Population"].sum().reset_index()
    top5 = state_pop.nlargest(5, "Population")
    fig = px.bar(top5, x="State", y="Population")
    st.plotly_chart(fig)
    st.subheader("What's inside? 👀")
    col1, col2 = st.columns(2)
    col1.info("📊 **State Analysis**\nWhich state has the highest population?")
    col2.warning("🏙️ **District Analysis**\nWhich district grew the fastest?")
elif page == "📊 State Analysis":
    st.title(" 📊 State Analysis")
    st.write("This page allows you to explore and compare multiple states of India side by side. Select one or more states from the dropdown below to get started. You can compare states on population, literacy rate, sex ratio and growth rate. The charts will automatically update based on your selection.")
    option = st.multiselect("Choose your states",sorted(df["State"].unique()),default=["Punjab", "West Bengal"]
    )
    if len(option) == 0:
        st.warning("Please select at least one state.")
        st.stop()
    selected_state = df[df["State"].isin(option)]
    st.divider()
    st.subheader("Literacy Gap ")
    st.write("Green means above average, Red means below.")
    avg = df["Literacy"].mean()
    st.write(f" Average Literacy: {avg:.1f}%")
    state_literacy = selected_state.groupby("State")["Literacy"].mean().reset_index()
    state_literacy["Gap"] = state_literacy["Literacy"] - avg
    fig = px.bar(state_literacy, x="State", y="Gap",
                     color="Gap",
                     color_continuous_scale=["red", "white", "green"],
                     color_continuous_midpoint=0,
                     labels={"Gap": " Literacy Gap (%)"})
    st.plotly_chart(fig)
    st.divider()
    st.subheader("State Comparison")
    st.write("Select a metric below to compare selected states.")
    comparison = selected_state.groupby("State").agg(
        Population = ("Population", "sum"),
        Literacy   = ("Literacy",   "mean"),
        Sex_Ratio  = ("Sex-Ratio",  "mean"),
        Growth     = ("Growth",     "mean")
    ).reset_index()
    metric = st.selectbox("Select metric to compare",["Population", "Literacy", "Sex_Ratio", "Growth"])

    fig = px.bar(comparison, x="State", y=metric,color="State",labels={metric: metric.replace("_", " ")})
    st.plotly_chart(fig)
    st.divider()
    st.subheader("Quick Numbers")
    cols = st.columns(len(option))
    for i, state in enumerate(option):
        state_data = selected_state[selected_state["State"] == state]
        with cols[i]:
            st.markdown(f"**{state}**")
            st.metric("Population",    f"{state_data['Population'].sum():,.0f}")
            st.metric("Avg Literacy",  f"{state_data['Literacy'].mean():.1f}%")
            st.metric("Avg Sex Ratio", f"{int(state_data['Sex-Ratio'].mean())}")
            st.metric("Avg Growth",    f"{state_data['Growth'].mean():.1f}%")

    st.divider()
elif page == "🏙️ District Analysis":
    st.title("🏙️ District Analysis")
    st.divider()
    st.write("This page allows you to explore any district in detail. First select a state and then select a district inside it. You will see a report card showing key metrics for that district, how it ranks among other districts in the same state, and charts showing the most populated and fastest growing districts.")
    state = st.selectbox("Select State",df["State"].unique()
    )
    state_df = df[df["State"] == state]
    st.divider()
    district = st.selectbox("Select District",state_df["District"].unique()
    )
    district_data = state_df[state_df["District"] == district]
    st.divider()
    st.subheader("📋 District Report Card")
    col1, col2, col3 , col4 = st.columns(4)
    col1.metric("Population",f"{district_data['Population'].values[0]:,}"
    )
    col2.metric("Literacy Rate",f"{district_data['Literacy'].values[0]}%"
    )
    col3.metric("Sex Ratio",district_data["Sex-Ratio"].values[0]
    )
    col4.metric("Growth Rate", f"{district_data['Growth'].values[0]}%")
    st.divider()
    population_rank      = state_df["Population"].rank(ascending=False)
    literacy_rank = state_df["Literacy"].rank(ascending=False)
    growth_rank   = state_df["Growth"].rank(ascending=False)
    district_population_rank = int(population_rank[state_df["District"] == district].values[0])
    district_literacy_rank = int(literacy_rank[state_df["District"] == district].values[0])
    district_growth_rank   = int(growth_rank[state_df["District"] == district].values[0])
    total = len(state_df)
    st.write(f"📊 **{district} ranks:**")
    st.write(f"- Population → **#{district_population_rank}** out of {total} districts in {state}")
    st.write(f"- Literacy → **#{district_literacy_rank}** out of {total} districts in {state}")
    st.write(f"- Growth → **#{district_growth_rank}** out of {total} districts in {state}")
    st.divider()
    st.subheader("Top 10 Most Populated Districts in " + state)
    top10 = state_df.nlargest(10, "Population")
    top10["Color"] = ["red" if d == district else "steelblue" for d in top10["District"]]
    fig = px.bar(top10, x="District", y="Population",
              color="Color",
              color_discrete_map={"red": "red", "steelblue": "steelblue"},
              labels={"Population": "Population", "Color": ""})
    st.plotly_chart(fig)
    st.divider()
    st.subheader("🏆 Top 5 Literacy Districts")
    top_literacy = state_df.nlargest(5, "Literacy")
    st.write(top_literacy[["District", "Literacy"]]
    )
    st.divider()
    st.subheader("📈 Top 10 Fastest Growing Districts")
    top_growth = state_df.nlargest(10, "Growth")
    fig = px.bar(
    top_growth,
    x="District",
    y="Growth",
    color="Growth"
   )
    st.plotly_chart(fig)
    st.write(top_growth[["District", "Growth"]])

