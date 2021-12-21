from tkinter import *
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

root = Tk()
root.title('Music Recommend')
root.geometry('700x700')


metadata = pd.read_csv('songs.csv', low_memory=False)
tfidf = TfidfVectorizer(stop_words='english')
metadata['Genres'] = metadata['Genres'].fillna('')
tfidf_matrix = tfidf.fit_transform(metadata['Genres'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
indices = pd.Series(metadata.index, index=metadata['song']).drop_duplicates()

songName = StringVar()
writerName = StringVar()
song = songName.get()
name = writerName.get()


def get_recommendations(song, cosine_sim=cosine_sim):
    # Get the index of the song that matches the song name
    idx = indices(song)

    # Get the pairwsie similarity scores of all songs with that song
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the song based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar songs
    sim_scores = sim_scores[1:11]

    # Get the song indices
    song_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar songs
    return metadata['song'].iloc[song_indices]


newSongs = get_recommendations(song)


def recommending():
    if entSongName.get():
        if entWriterName.get():
            lblRecommend.config(text=newSongs)
        else:
            entWriterName.focus_set()
    else:
        entSongName.focus_set()


# Labels
lblTitle = Label(root, text='Music Title', font=('arial', 18, 'bold'))
lblTitle.place(x=10, y=10)

lblWriter = Label(root, text='Artist or Songwriter', font=('arial', 18, 'bold'))
lblWriter.place(x=10, y=60)

lblRecommended = Label(root, text='Recommended Songs', font=('arial', 18, 'bold'))
lblRecommended.place(x=10, y=200)

# Text Fields

entSongName = Entry(root, textvariable=songName, font=('arial', 10, 'bold'), bg='lightgrey', width=40)
entSongName.place(x=300, y=10)

entWriterName = Entry(root, textvariable=writerName, font=('arial', 10, 'bold'), bg='lightgrey', width=40)
entWriterName.place(x=300, y=60)

# Button

btnSubmit = Button(root, text='Submit', font=('arial', 18, 'bold'), command=recommending)
btnSubmit.place(x=300, y=120)
btnSubmit.config(bg='#4a90cc', fg='black')

lblRecommend = Label(root, text="", font=('Times New Roman', 10, 'bold'), height=30, justify='left')
lblRecommend.place(x=300, y=200)
lblRecommend.config(bg='#ccaf4a', fg='black', width=40)

root.mainloop()
