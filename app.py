from flask import Flask, render_template, request
import requests
import random
import os
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()

# replace with your personal bearer token
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    data1, data2 = None, None
    cleared = ''

    if request.method == 'POST':
        num1 = random.randint(1, 933)
        page_num = random.randint(1, 3)
        num2 = random.randint(1, 1000)
        if page_num == 3:
            num2 = random.randint(1, 384)

        api_endpoint1 = 'https://the-one-api.dev/v2/character'
        api_endpoint2 = 'https://the-one-api.dev/v2/quote?page={page_num}'
        api_endpoint_movies = 'https://the-one-api.dev/v2/movie'
        headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
        response1 = requests.get(api_endpoint1, headers=headers)
        data1 = response1.json()
        chars_dict = {}
        for i in range(933):
            char_obj = data1['docs'][i]
            specific_char = data1['docs'][i]['name']
            chars_dict[specific_char] = char_obj['_id']

        response2 = requests.get(api_endpoint2, headers=headers)
        data2 = response2.json()

        response3 = requests.get(api_endpoint_movies, headers=headers)
        data3 = response3.json()
        movies_dict = {}
        for i in range(2, 8):
            movie = data3['docs'][i]
            specific_movie = data3['docs'][i]['name']
            movies_dict[specific_movie] = movie['_id']

        # getting character info
        character = data1['docs'][num1]
        name = character['name']
        if name == 'NaN' or name == '':
            name = 'Unknown'
        race = character['race']
        if race == 'NaN' or race == '':
            race = 'Unknown'
        gender = character['gender']
        if gender == 'NaN' or gender == '':
            gender = 'Unknown'
        birth = character['birth']
        if birth == 'NaN' or birth == '':
            birth = 'Unknown'
        death = character['death']
        if death == 'NaN' or death == '':
            death = 'Unknown or still living'
        char_string = f'Name: {name}, Race: {race}, Gender: {gender}, Birth: {birth}, Death: {death}'

        # getting quote info
        quote = data2['docs'][num2]
        dialogue = quote['dialog']
        movie = quote['movie']
        for name, id in movies_dict.items():
            if movie == id:
                movie = name
        char = quote['character']
        for name, id in chars_dict.items():
            if char == id:
                char = name
        quote_string = f'Quote: "{dialogue}", Movie: {movie}, Character: {char}'

        button_value = request.form['button']
        if button_value == 'get_char':
            print(movies_dict)
            return render_template('index.html', text=char_string)
        if button_value == 'get_quote':
            return render_template('index.html', text=quote_string)
        else:
            return render_template('index.html', text=cleared)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
