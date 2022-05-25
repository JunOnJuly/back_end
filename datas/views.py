from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import random

@api_view(['GET'])
# 영화 추천
def get_genre_movie(request, lat, lon):
    def index_to_weather(lat, lon):
        api_key = '57c5fccaf8db3eeceae84f1b23155ed9'
        add = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'

        response = requests.get(add).json()
        weather_data = response['weather'][0]['description']
        return weather_data

    # 음악정보 받아오기
    def weather_to_music_genre(weather):
        weather_to_music = {
            'sun': ['Children', 'Latin', 'Disco', 'Funk', 'Hiphop', 'Reggae', 'Country'],
            'clear': ['Children', 'Latin', 'Disco', 'Funk', 'Hiphop', 'Reggae', 'Country'],
            'snow': ['Children', 'Jazz', 'Newage', 'Christian'],
            'rain': ["R&B", 'Jazz', 'Classical', 'Blues', 'Newage', 'Country'],
            'Cloudy': ["R&B", 'Jazz', 'Classical', 'Blues', 'Newage', 'Country'],
            'Fog': ["R&B", 'Jazz', 'Classical', 'Blues', 'Newage', 'Country'],
            'Storm': ['Rock', 'Funk', 'Christian'],
            'Lightning': ['Rock', 'Country'],
            'Hail': ['Rock', 'Christian', 'Disco', 'Funk'],
            'Flood': ['Rock', 'Christian'],
            'Fire': ['Rock', 'Christian'],
            'Rainbow': ['Newage', 'Jazz', 'Hiphop', 'Disco']
        }

        for key in weather_to_music.keys():

            if key.find(weather):
                genre_list = [random.choice(weather_to_music[key])]
            else:
                genre_list = random.sample(weather_to_music[random.choice(weather_to_music.keys())], 2)
        return genre_list

    def music_genre_to_movie_genre(music_genre):
        music_to_movie = {
            'Rock': ['Action', 'Comedy','Crime'],
            'R&B': ['Documentary', 'Drama', 'Family', 'Romance'],
            'Reggae': ['Action', 'Comedy'],
            'Country': ['Western', 'Comedy'],
            'Funk': ['Action'],
            'Christian': ['Documentary', 'Drama', 'History', 'Horror'],
            'Jazz': ['Comedy', 'History'],
            'Disco': ['Comedy', 'Adventure', 'Fantasy'],
            'Classical': ['Documentary', 'Drama', 'History', 'Science Fiction', 'Mystery', 'Horror', 'Thriller'],
            'Latin': ['Action', 'Comedy'],
            'Blues': ['Romance', 'History'],
            'Children': ['Family', 'Animation', 'Comedy'],
            'Newage': ['Animation', 'Science', 'Documentary', 'Mystery', 'Family', 'Drama', 'War'],
            'pop': ['Adventure', 'Fantasy']
        }

        movie_list = []

        for key in music_to_movie.keys():
            for genre in music_genre:
                if key == genre:
                    if len(music_to_movie[genre]) > 2:
                        movie_list.extend(random.sample(music_to_movie[genre], 2))
                    else:
                        movie_list.extend(music_to_movie[genre])
                    break
            
        return movie_list
        
    def get_movies_data(genre):
        genre_string = ', '.join(genre)
        api_key = 'e9358ffd6481eecb3dbe07e8d1d534ea'
        add = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre_string}&sort_by=vote_average.desc'
        response = requests.get(add).json()
        movie_data = response['results']
        return movie_data
    
    weather = index_to_weather(lon, lat)
    genre_list = weather_to_music_genre(weather)
    movie_genre = music_genre_to_movie_genre(genre_list)
    movie_data = get_movies_data(movie_genre)

    return Response(movie_data)

@api_view(['GET'])
# 음악 추천
def get_genre_music(request, lat, lon):
    # 날씨정보 받아오기
    def index_to_weather(lat, lon):
        api_key = '57c5fccaf8db3eeceae84f1b23155ed9'
        add = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'

        response = requests.get(add).json()
        weather_data = response["weather"][0]['description']
        return weather_data

    # 음악정보 받아오기
    def weather_to_music_genre(weather):
        weather_to_music = {
            'sun': ['Children', 'Latin', 'Disco', 'Funk', 'Hiphop', 'Reggae', 'Country'],
            'snow': ['Children', 'Jazz', 'Newage', 'Christian'],
            'rain': ["R&B", 'Jazz', 'Classical', 'Blues', 'Newage', 'Country'],
            'Cloudy': ["R&B", 'Jazz', 'Classical', 'Blues', 'Newage', 'Country'],
            'Fog': ["R&B", 'Jazz', 'Classical', 'Blues', 'Newage', 'Country'],
            'Storm': ['Rock', 'Funk', 'Christian'],
            'Lightning': ['Rock', 'Country'],
            'Hail': ['Rock', 'Christian', 'Disco', 'Funk'],
            'Flood': ['Rock', 'Christian'],
            'Fire': ['Rock', 'Christian'],
            'Rainbow': ['Newage', 'Jazz', 'Hiphop', 'Disco']
        }

        selected_music = {
            'posters': [],
            'titles': []
        }

        for key in weather_to_music.keys():

            if key.find(weather):
                genre_list = random.choice(weather_to_music[key])
            else:
                genre_list = random.sample(weather_to_music['Rainbow'], 2)
        
        for genre in genre_list:
            url = "https://spotify23.p.rapidapi.com/search/"
            querystring = {"q":{genre},"type":"genre","offset":"0","limit":"10","numberOfTopResults":"5"}
            headers = {
                "X-RapidAPI-Host": "spotify23.p.rapidapi.com",
                "X-RapidAPI-Key": "b041bf3092msh18b2132f590d186p14d298jsn627b3c07b2ec"
            }
            response = requests.request("GET", url, headers=headers, params=querystring).json()
            choice_num = random.sample(range(len(response['albums']['items'])), 5)

            for num in choice_num:
                selected_music['posters'].append(response['albums']['items'][num]['data']['coverArt']['sources'][-1]['url'])
                selected_music['titles'].append(response['albums']['items'][num]['data']['name'])
        
        

        return Response(selected_music)

    weather = index_to_weather(lon, lat)

    return weather_to_music_genre(weather)


@api_view(['GET'])
def find_ost(request, movie_title):
    url = "https://spotify23.p.rapidapi.com/search/"
    querystring = {"q":{movie_title},"type":"albums","offset":"0","limit":"10","numberOfTopResults":"5"}
    headers = {
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com",
        "X-RapidAPI-Key": "b041bf3092msh18b2132f590d186p14d298jsn627b3c07b2ec"
    }
    response = requests.request("GET", url, headers=headers, params=querystring).json()['albums']['items']
    music_datas = {
        'titles': [],
        'cover_urls': [],
    }
    for music_data in response:
        music_datas['cover_urls'].append(music_data['data']['coverArt']['sources'][-1]["url"])
        music_datas['titles'].append(music_data['data']['name'])

    return Response(music_datas)