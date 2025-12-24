import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
st.title("population")
df = pd.read_csv("census2011.csv")
st.write(df)
df["Population"] = (
    df["Population"]
    .astype(str)
    .str.replace(",", "", regex=True)
)
df["Population"] = pd.to_numeric(df["Population"].astype(int))
option=st.multiselect ("choose your state",
                      df["State"], default=["Punjab","West Bengal"])
selected_state= df[df["State"].isin(option)]
st.write(selected_state)
fig=px.sunburst(selected_state,path= ["State","District"],values="Population")
st.plotly_chart(fig)