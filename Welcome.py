import streamlit as st
import pandas as pd
import requests
import pickle
import numpy as np
import sqlite3

#set the page config
st.set_page_config(layout='wide', initial_sidebar_state='expanded',page_title="Festival Matchmaker",
    page_icon="🤘")
    
st.sidebar.header('🤘 Festival Matchmaker')

st.sidebar.markdown('''
---
Made by Carolina L. Shimabukuro

⭐⭐⭐

''')

# page content
st.title("""
Festival Matchmaker 🤘!
""")

st.subheader("""
Which festival should I go to? :thinking_face:
""")

st.write("""
    Every year I have the same problem: too many festivals, too little time (and money!).
    I built this little app to help me choose which festival to go to 
    according to how well their lineups match [my taste](https://www.last.fm/user/caro_g), instead of
    sitting for hours checking out each individual artist in a lineup. I mean, I probably will still do that, but
    at least I will know what to check out first!

    You can find the repo for this app and a couple of notebooks [here](https://github.com/carolinashima/festival-matchmaker).
    """
)

st.subheader("Some caveats")
st.write("""
    * My user profile was built with my top 150 artists, which I think is representative of my general taste in music
    but is also biased against post-rock, for example.
    * Artist similarity was calculated by retrieving tags on Last.fm, so: 1) I wasn't able to calculate similarity for
    very small artists that haven't been scrobbled; 2) tags are added manually by users, so a bunch of them are either not
    related to genre or are sometimes just [weird/funny](https://www.last.fm/tag/if+this+were+a+pokemon+i+would+catch+it).
    * Artists with special characters (e.g. &) were not processed correctly with the Last.fm API so I have no similarity scores
    for them either.
    * The 40 festivals were chosen manually by looking at Setlist.fm's lists of festivals in 2024. Partly because I had to
    scrape them and partly because I'm probably not interested in attending most festivals that exist in the world.
""")

st.subheader("Future improvements/to do")
st.write("""
    * I suspect that scores would be more accurate if I was using genre information that is not based on user generated tags,
    or if I spent more time filtering useless ones (e.g. "seen live").
    * Ideally this could be expanded and applied to any person with *some* music data (e.g. streaming services) and any
    event (unfortunately Songkick's API is not available anymore so if you know of any alternative, please let me know).
""")

# load festival summary
with open('festival_summary.pkl', 'rb') as f:
    festival_summary = pickle.load(f)
st.session_state['festival_summary'] = festival_summary

# connect to db
conn = sqlite3.connect('festival_data.db')
cursor = conn.cursor()

# query db to get festival data
cursor.execute('SELECT festival_name, data FROM festival_data')
rows = cursor.fetchall()

# deserialise data and put in dict
festival_data = {}
for festival_name, serialized_data in rows:
    # deserialise, put in df
    df = pickle.loads(serialized_data)
    # put df in dict
    festival_data[festival_name] = df
# close connection
conn.close()

sorted_dict = dict(sorted(festival_data.items()))
st.session_state['festival_data'] = sorted_dict

