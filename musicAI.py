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
song = StringVar()
name = writerName.get()


def recommending():
    if entSongName.get():
        if entWriterName.get():
            def get_recommendations(song, cosine_sim=cosine_sim):
                # Get the index of the song that matches the song name
                idx = indices[song]

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

            newSongs = get_recommendations(songName.get())
            lblRecommend.config(text=newSongs)
        else:
            entWriterName.focus_set()
    else:
        entSongName.focus_set()


# Labels
lblTitle = Label(root, text='Song Title', font=('arial', 18))
lblTitle.place(x=155, y=10)

lblWriter = Label(root, text='Artist or Songwriter', font=('arial', 18))
lblWriter.place(x=60, y=60)

lblRecommended = Label(root, text='Recommended Songs', font=('arial', 18))
lblRecommended.place(x=30, y=200)

# Text Fields

entSongName = Entry(root, textvariable=songName, font=('arial', 18, 'bold'), width=30)
entSongName.place(x=300, y=10)

entWriterName = Entry(root, textvariable=writerName, font=('arial', 18, 'bold'), width=30)
entWriterName.place(x=300, y=60)

# Button

btnSubmit = Button(root, text='Submit', font=('arial', 18), command=recommending, width=10)
btnSubmit.place(x=300, y=120)
btnSubmit.config(bg='#3b4b9c', fg='white')

lblRecommend = Label(root, text="", font=('Times New Roman', 10, 'bold'), height=30, justify='left')
lblRecommend.place(x=300, y=200)
lblRecommend.config(bg='#c37212', fg='black', width=40)

root.mainloop()
