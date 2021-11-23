import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
st.title("just think of everything else i could be doing than coming up with a funny title")
@st.cache
def load_data():
    data = pd.read_csv('C:/Users/barre/python stuff/data/score_df.csv')
    data = data.rename(columns = {'Unnamed: 0' : 'generation'
    })
    return data

def get_best_ind(df, generation):
    return df.loc[generation, 'individual']


def load_individual(individual):
    run_game_vis(individual)
    return

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data()
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")
if st.checkbox('Show Raw Data'):
    st.subheader('Raw Data')
    st.write(data)

st.subheader('Performance by Generation: ')

chart = alt.Chart(data).mark_line().encode(
  x='generation',
  y='max score',
).properties(title="Performance by Generation")
st.altair_chart(chart, use_container_width=True)