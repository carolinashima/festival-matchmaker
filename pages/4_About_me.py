import streamlit as st

st.set_page_config(layout='wide', initial_sidebar_state='expanded',page_title="Festival Matchmaker",
    page_icon="🤘")

    
st.sidebar.header('🤘 Festival Matchmaker')
st.sidebar.markdown('''
---
Made by Carolina L. Shimabukuro

⭐⭐⭐

''')

# page content
st.title("About me 👩🏻‍💻")
col1, col2 = st.columns([0.6, 0.4], gap = "small")

with col1:
    st.write("""
    Hi! :wave: I'm Carolina.
    
    I'm originally from Buenos Aires, Argentina, but currently based in Berlin, Germany.
    I love music and traveling but most of all traveling to some concert: hence this little project!
    (Although to be fair most of the time I just go to the UK to see Liam Gallagher 😅)

    If you have any feedback or comments feel free to [contact me](https://linktr.ee/carolinashima).
    """)

with col2:
    st.image(".static/foto_polo.jpg",
    "My doggie Apolo and I, Buenos Aires, Argentina, May 2015", width=300)