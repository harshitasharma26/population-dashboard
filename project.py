import streamlit as st
import pandas as pd
st.title("population")
df = pd.read_csv("census2011.csv")
st.write(df)
option=st.multiselect("choose your state",
                      df["State"],placeholder= "typing")
selected_state= df[df["State"].isin(option)]
st.write(selected_state)
record=st.selectbox("choose your state",
                      df["State"],placeholder= "typing")
selected= df[df["State"]==record]
st.write(selected)
            