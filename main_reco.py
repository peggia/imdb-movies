
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils.ml_model import init_model, get_recommendations

#Page configuration
st.set_page_config(
    page_title="IMDB Movies Recommendations",
    page_icon="📽️",
    layout="wide"
)
#
st.title("IMDB Movies Recommendations")

@st.cache_data
def get_data():
    # REPOSITORY: definir l'adresse vers le bon dataset sur GitHub
    link = "https://raw.githubusercontent.com/peggia/latam-movies/refs/heads/main/grouped_movies_latam_ML.csv"
    df= pd.read_csv(link,sep =';')
    return df

def get_poster_path(title,df):
    base_path = 'https://image.tmdb.org/t/p/original'
    element = df[df['fullTitle'] == title]
    return base_path + element["poster_path"].values[0] 

# Barre latérale pour la navigation entre les sections
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to:", 
                           ["Latam Movies",
                            "French Movies", 
                            ])
    
#main page
#
if section == "Latam Movies":
    df_movies = get_data()

    st.write("### Latin American Movies")
    st.write('List of movies')
    
    # display list selection
    with st.form(key='my_form'):
        selected_movies = st.multiselect('Select movies or start typing a title',
                                        options=df_movies['fullTitle'].tolist(),
                                        help='Start typing the name of a movie, then pick from the list.'
                                        )
         # FILTERING OPTION 1
        with st.expander('Filtering Options', expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                min_year = df_movies['startYear'].min()
                max_year = df_movies['startYear'].max()
                year_range = st.slider('Year Range', min_value=min_year, max_value=max_year, 
                                       value=(min_year, max_year))
                 # Further filter DataFrame based on selected year range
                filtered_df = df_movies[(df_movies['startYear'] >= year_range[0]) & (df_movies['startYear'] <= year_range[1])]
            with col2:
                #extract the list of genres from column 'genres'
                genres= set()
                for genre in df_movies['genres']:
                  genres.update(genre.split(' '))
                genres = list(genres)
                selected_genres = st.multiselect('Genre(s)',genres,help='Start typing the name of a genre, then pick from the list.' )
                #filtrer movies en utilisant le genre selectionné par l'utilisataeur
                
        #----------
        posters = []
        for i in range(len(selected_movies)):
            posters.append(get_poster_path(selected_movies[i],df_movies))
        st.image(posters,width=100)
        submit_button = st.form_submit_button(label='Find similar Movies 🎬', type='primary')
         #----------
        similarity = init_model(df_movies['combined_features'])
        if submit_button:
            with st.spinner('Finding similar movies...'):
                #get the similar movies df
 
                similar_movies = get_recommendations(selected_movies,df_movies,similarity)
 
                #display and next step : https://docs.streamlit.io/develop/tutorials/elements/dataframe-row-selections
                st.dataframe(
                    similar_movies[['fullTitle','startYear','genres','directors','production_countries','averageRating',
                                    'numVotes',]].head(100), hide_index=True,
                    column_config={
                         
                           "fullTitle": st.column_config.TextColumn(
                                "Title", width="large"
                            ),
                            "startYear": st.column_config.NumberColumn(
                                "startYear", width="small"
                            ),
                            "directors": st.column_config.TextColumn(
                                "Directors", width="medium"
                            ),
                            "production_countries": st.column_config.TextColumn(
                                "Countries", width="small"
                            ),
                            "genres": st.column_config.TextColumn(
                                "Genres", width="Medium"
                            ),
                            "averageRating": st.column_config.NumberColumn(
                                "imdb Rating",
                                format="%.1f", width="small",
                            ),
                            "numVotes": st.column_config.NumberColumn(
                                "# of Votes",
                                format="%.0f", width="small",
                            )


                    }         
                )

# ---------------------------------------------------------------------------
# Section 2 : 
# ---------------------------------------------------------------------------
elif section == "French Movies":    
    st.write("### French Movies... coming soon!")
    st.write('List of movies')
# except URLError as e:
#     st.error(
#         """
#         **This demo requires internet access.**
#         Connection error: %s
#     """
#         % e.reason
#     )
