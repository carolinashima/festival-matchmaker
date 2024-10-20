import streamlit as st
import pandas as pd

st.set_page_config(layout='wide', initial_sidebar_state='expanded',page_title="Festival Matchmaker",
    page_icon="🤘")

    
st.sidebar.header(':the_horns: Festival Matchmaker')
st.sidebar.markdown('''
---
Made by Carolina L. Shimabukuro

⭐⭐⭐

''')

st.title("Best match :heart:")
st.write("""
So, which festival should I go to?
""")
selected_cols = ["festi_name","n_artists","mean_score","median_score"]
sorted_df = st.session_state["festival_summary"][selected_cols].sort_values(by='median_score', ascending = False)
sorted_df["Rank"] = range(1, len(sorted_df) + 1)
sorted_df.set_index("Rank", inplace = True)

# winner!
winner = sorted_df.iloc[0]["festi_name"]

# display
st.write(f":tada: The winner is...")
font_size = 50
html_str = f"""
<style>
p.a {{
  font: bold {font_size}px Source sans pro;
}}
</style>
<p class="a">{winner}!</p>
"""
st.markdown(html_str, unsafe_allow_html=True)
st.write("""
    Let's take a look at the festival rankings.
    The winner is the one with the highest **median** score.
""")
# display table
st.dataframe(sorted_df,
    column_config = {
        "festi_name": "Festival",
        "n_artists": "N artists",
        "mean_score": "Mean score",
        "median_score": "Median score"})
    #},
    #hide_index=True)
