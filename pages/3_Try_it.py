import streamlit as st
import pandas as pd
import requests
from math import sqrt
from collections import defaultdict
import pickle
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen

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

st.title("Try it! :microphone:")

st.write("""
If you have a [Last.fm](https://www.last.fm) account, give it a try! Enter your username and paste the URL
to any festival listed on [Setlist.fm](https://www.setlist.fm/festivals).
Scores will be calculated with your overall top 50 artists and not weighted by scrobbles.
""")

# build user profile
username = st.text_input("Enter Last.fm username", value = 'caro_g')

# input festival to scrape
default_url = 'https://www.setlist.fm/festival/2025/primavera-sound-2025-bd5898e.html'
festi_url = st.text_input("Enter Setlist.fm festival link", value = default_url)

#load_dotenv()
#API_KEY = os.getenv('API_KEY')
API_KEY = st.secrets["API_KEY"]

library_artists_features = dict()
#n_top_artists = 50 # arbitrary number of artists to build profile

url = f'http://ws.audioscrobbler.com/2.0/?method=user.getTopArtists&user={username}&api_key={API_KEY}&format=json&limit=20'

with st.spinner("Calculating scores... (this might take some time :sleeping:)"):
    # get top artists from last.fm
    try:
        response = requests.get(url)
        response.raise_for_status()
        artistdata = response.json()
        artists_list = []
        artists_scrobbles = []
        try:
            for artist in artistdata['topartists']['artist']:
                artists_list.append(artist['name'])
                artists_scrobbles.append(int(artist['playcount']))
        except:
            print(f"Artist: {artist}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

    df = pd.DataFrame({
        'artist': artists_list,
        'scrobbles': artists_scrobbles
    })

    # artist names as keys, and a list of tags as values
    for artist in df["artist"]:
        url = f'http://ws.audioscrobbler.com/2.0/?method=artist.getTopTags&artist={artist}&api_key={API_KEY}&format=json&limit=20'
        try:
            response = requests.get(url)
            response.raise_for_status()
            artistdata = response.json()
            these_tags = []
            try:
                for tagname in artistdata['toptags']['tag']:
                    if tagname['name'] == 'seen live': # exclude seen live
                        continue
                    these_tags.append(tagname['name'])
            except:
                print(f"Artist: {artist}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            
        library_artists_features[artist] = {'tags': these_tags}

    # turn df into dict, artist: number of scrobbles
    listening_history = dict(df.values)

    # user profile function
    def construct_user_profile(library_artists_features, listening_history):
        profile = defaultdict(float)
        total_listens = sum(listening_history.values())

        for artist, listens in listening_history.items():
            for tag in library_artists_features[artist]['tags']:
                profile[tag] += listens / total_listens

        return profile

    # calculate user profile
    user_profile = construct_user_profile(library_artists_features, listening_history)

    # define cosine similarity
    def cosine_similarity(profile, artist_features):
        dot_product = sum(profile[feature] * artist_features.get(feature, 0) for feature in profile)
        profile_magnitude = sqrt(sum(value ** 2 for value in profile.values()))
        artist_magnitude = sqrt(sum(value ** 2 for value in artist_features.values()))
        
        if profile_magnitude == 0 or artist_magnitude == 0:
            return 0.0
        return dot_product / (profile_magnitude * artist_magnitude)

    # function to scrape festival lineups as they appear in setlist.fm
    def scrape_setlistfm(festival_url):
        # Read html
        html = urlopen(festival_url).read()
        # Parse
        soupified = BeautifulSoup(html, 'html.parser')

        #festi_name = soupified.title.string
        headerr = soupified.find('h1')
        festi_name = headerr.get_text()
        artists_list = soupified.find_all(attrs={"class": "FestivalSetlistListItem-artist"})
        
        lineup = []
        for artist in artists_list:
            a = artist.find("a", {"class": "Link-root_color-blue"}).get_text().strip()
            lineup.append(a)
        
        # get general data like dates, venue, etc.
        date_div = soupified.find('div', class_='festivalContent')
        if date_div:
            for span in date_div.find_all('span'):
                text = span.get_text().strip()
                if ' - ' in text and ',' in text: # format example: Wednesday, August 21, 2024 - Sunday, August 25, 2024
                    date_text = text
                    break
        
        # venue
        venue_tag = soupified.find('h2', class_='Text-root Text-root_variant-display2 Text-root_color-grayDark')
        venue_text = venue_tag.get_text(strip=True)

        return festi_name, lineup, date_text, venue_text


    # scrape!
    festi_name, lineup, festi_date, festi_venue = scrape_setlistfm(festi_url)

    # calculate similarities
    n_tags = 10 # get the top 10 tags


    artists_scores = dict()
    for artist in lineup:
    #for artist in artist_list:
        url = f'http://ws.audioscrobbler.com/2.0/?method=artist.getTopTags&artist={artist}&api_key={API_KEY}&format=json&limit=20'
        try:
            response = requests.get(url)
            response.raise_for_status()
            artistdata = response.json()

            if 'error' in artistdata: # error 6, artist could not be found
                #artists_scores[artist] = float("nan")
                artists_scores[artist] = None
            else:

                newband_vector = dict()
                try:
                    for tagname in artistdata['toptags']['tag'][:n_tags]:
                        if tagname['name'] == 'seen live': # exclude seen live
                            continue
                        newband_vector[tagname['name']] = tagname['count']
                except:
                    print(f"Artist error: {artist}")
                    print(f"{artistdata}")

                sum_vals = sum(newband_vector.values())
                newband_vector_scaled = {k: v / total for total in (sum(newband_vector.values()),) for k, v in newband_vector.items()}
                similarity_score = cosine_similarity(user_profile, newband_vector)
                #print(f"{artist}: {similarity_score:.2f}")
                artists_scores[artist] = similarity_score
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")

# convert to df
final_df = pd.DataFrame(list(artists_scores.items()), columns=['Artist', 'Score'])
sorted_df = final_df.sort_values(by='Score', ascending = False)

# display
word_to_cut = 'Setlists'
index = festi_name.find(word_to_cut)
festi_name_short = festi_name[0:index]
st.subheader(festi_name_short)

#n_artists = len(sorted_df)
median_score = sorted_df['Score'].median()

# display date and venue
st.write("**Date and venue**:")
st.write(f"{festi_date}")
st.write(f"{festi_venue}")

st.metric("**Median score**", round(median_score,2))
st.dataframe(sorted_df, hide_index=True)