import streamlit as st
import pandas as pd
import requests
import pickle
import numpy as np
import sqlite3

#set the page config
st.set_page_config(layout='wide', initial_sidebar_state='expanded',page_title="Festival Matchmaker",
    page_icon="🤘")
    
st.sidebar.header(':the_horns: Festival Matchmaker')

st.sidebar.markdown('''
---
Made by Carolina L. Shimabukuro

⭐⭐⭐

''')

# page content
st.title("""
Festival Matchmaker :the_horns:!
""")

st.subheader("""
Which festival should I go to? :thinking_face:
""")

st.write("""
    Every year, the same problem: too many festivals, too little time (and money!).
    This little app was built to help me choose which festival to go to 
    according to how well their lineups match my taste.
    """
    # write more about how I did this!
)


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

