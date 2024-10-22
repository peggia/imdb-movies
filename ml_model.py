import pandas as pd
import numpy as np
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# we choose to use the fullTitle (combination of original - primary titles if they are different)
# def combine_features(row):
#     return row['fullTitle']+' '+row['genres']+' '+row['actors'] +' '+row['writerName']+' '+row['directorName']

#Helper functions
def get_index_from_title(title,df):
  element = df[df['fullTitle'] == title]
  return element["index"].values[0]
    
@st.cache_resource
def init_model(features_column):
  #create a new column with combined features
  # df['combined_features'] = df.apply(combine_features, axis = 1)
  # df.reset_index(drop=True, inplace=True)
  # df['index'] = df.index

  #fit and transform the count vectorizer model
  cv = CountVectorizer()
  count_matrix = cv.fit_transform(features_column)
  cosine_sim = cosine_similarity(count_matrix)
  return cosine_sim
    
#function to import in the main program
def get_recommendations(selected_movies,df,cosine_sim):
    #get indexes for selected_movies
    sorted_similar_movies = []
    for title in selected_movies:
        movie_index = get_index_from_title(title,df)

        #all the similarity scores for that movie and then enumerating over it
        similar_movies =  list(enumerate(cosine_sim[movie_index]))

        #sort similar movies by similarity score and keep 10 excluding the first (element itself)
        sorted_similar_movies.append(sorted(similar_movies,key=lambda x:x[1],reverse=True)[0:11])

    #build the df to return
    indices_list = []
    i=0
    for element in sorted_similar_movies:
        # Extract only the indices from the tuples
        indices_list.extend([x[0] for x in element])  
    
    similar_movies_df = df.iloc[indices_list].drop(columns = ['combined_features','index'])
    return similar_movies_df