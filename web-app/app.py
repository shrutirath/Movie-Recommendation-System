from flask import Flask, render_template, request
import pickle
import pandas as pd
import requests
app = Flask(__name__)

data = pd.read_csv("movie_data_with_tags.csv")
similarity = pickle.load(open('similarity.pkl', 'rb'))

@app.route('/')
def hello():
    return render_template("index.html")
    


def recommend(movies):
    movies_index = data[data['title'] == movies].index[0]
    distances = similarity[movies_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:9]
    movies_name = []
    for i in movies_list:
        print(data.iloc[i[0]].title)
        movies_name.append(data.iloc[i[0]].id)

    return movies_list


def fetch(movie_id):
    URL = 'https://api.themoviedb.org/3/movie/{}?api_key=6aeea4409e82ad77bfbe5f7beb516560&language=en-US'.format(movie_id)
    response = requests.get(URL)
    ans = response.json()
    return ans

@app.route('/recommendations', methods=['POST'])
def getmovies():
    if request.method == "POST":
        movie = request.form["movie"]
        print(movie)
        movie_list = recommend(movie)

        movie_name = []
        movie_poster = []

        for i in movie_list:
            movie_id = data.iloc[i[0]].id
            movie_details = fetch(movie_id)

            poster_path = 'https://image.tmdb.org/t/p/w500' + movie_details['poster_path']
            movie_name.append(data.iloc[i[0]].title)
            movie_poster.append(poster_path)

        return render_template("recommend.html", name=movie_name, poster = movie_poster)
        # return render_template("recommend.html")





if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8000, debug=True)
    app.run(host='0.0.0.0', port=8000)
