import streamlit as st
import pandas as pd


#set the page config
st.set_page_config(layout='wide', initial_sidebar_state='expanded',page_title="Festival Matchmaker",
    page_icon="🤘")

    
st.sidebar.header(':the_horns: Festival Matchmaker')
#st.subheader('Indicator')


st.sidebar.markdown('''
---
Made by Carolina L. Shimabukuro

⭐⭐⭐
''')
st.title("Lineups :guitar:")
st.write("""
OK but who's playing each festival
and what are their individual scores?
""")
st.write("""
Choose a festival from the dropdown menu to see its lineup
and each artist's scores.
""")

# retrieve data
festival_data = st.session_state["festival_data"]
selected_festival = st.selectbox('Choose a festival', festival_data.keys())
# retrieve summary df
festival_summary = st.session_state['festival_summary']

# display date and venue
festi_date = festival_summary[festival_summary["festi_name"]==selected_festival]["date"].values[0]
festi_venue = festival_summary[festival_summary["festi_name"]==selected_festival]["venue"].values[0]

st.write("**Date and venue**:")
st.write(f"{festi_date}")
st.write(f"{festi_venue}")

this_median = festival_summary[festival_summary["festi_name"]==selected_festival]["median_score"]
st.metric("**Median score**", round(this_median,2))

selected_cols = ["artist_name","cosine_similarity","scrobbles_norm","scrobbles","final_score"]
sorted_df = festival_data[selected_festival][selected_cols].sort_values(by='final_score', ascending = False)


if selected_festival:
    st.write(f"**{selected_festival}** lineup scores:")
    #st.write(f"Date: {festi_date}")
    #st.dataframe(festival_data[selected_festival], hide_index=True)
    st.dataframe(sorted_df,
    column_config = {
        "artist_name": "Artist",
        "cosine_similarity": "Cosine similarity",
        "scrobbles_norm": "Scrobbles (normalised)",
        "scrobbles": "Scrobbles",
        "final_score": "Final score"
    },hide_index=True)

# new
#sorted_df["Rank"] = range(1, len(sorted_df) + 1)
#sorted_df.set_index("Rank", inplace = True)


