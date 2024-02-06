from flask import Flask, render_template, request
import requests
# import random
import os
from dotenv import load_dotenv
import zmq


app = Flask(__name__)

load_dotenv()

# replace with your personal bearer token
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')

# ZeroMQ setup
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")


def generate_random_numbers():
    socket.send_string("generate_numbers")
    response = socket.recv_json()
    return response["num1"], response["page_num"], response["num2"]


# Initialize chars_dict and  movies_dict
chars_dict = {}
movies_dict = {}


def initialize_dicts():
    global chars_dict, movies_dict
    api_endpoint1 = 'https://the-one-api.dev/v2/character'
    api_endpoint_movies = 'https://the-one-api.dev/v2/movie'
    headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}

    # Initialize chars_dict
    response1 = requests.get(api_endpoint1, headers=headers)
    data1 = response1.json()
    chars_dict = {}
    for i in range(933):
        char_obj = data1['docs'][i]
        specific_char = data1['docs'][i]['name']
        chars_dict[specific_char] = char_obj['_id']

    # Initialize movies_dict
    response3 = requests.get(api_endpoint_movies, headers=headers)
    data3 = response3.json()
    movies_dict = {}
    for i in range(2, 8):
        movie = data3['docs'][i]
        specific_movie = data3['docs'][i]['name']
        movies_dict[specific_movie] = movie['_id']


# Call the function to initialize both dictionaries when the app starts
initialize_dicts()


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    global chars_dict, movies_dict

    data1, data2 = None, None
    cleared = ''

    if request.method == 'POST':
        num1, page_num, num2 = generate_random_numbers()
        # num1 = random.randint(1, 933)
        # page_num = random.randint(1, 3)
        # num2 = random.randint(1, 1000)
        # if page_num == 3:
        #     num2 = random.randint(1, 384)

        api_endpoint1 = 'https://the-one-api.dev/v2/character'
        api_endpoint2 = 'https://the-one-api.dev/v2/quote?page={page_num}'

        headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
        response1 = requests.get(api_endpoint1, headers=headers)
        data1 = response1.json()

        response2 = requests.get(api_endpoint2, headers=headers)
        data2 = response2.json()

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

        # Display movie name and character name for quote
        # instead of movie_id and char_id
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
            return render_template('index.html', text=char_string)
        if button_value == 'get_quote':
            print(movies_dict)
            return render_template('index.html', text=quote_string)
        else:
            return render_template('index.html', text=cleared)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
