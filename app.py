from flask import Flask, render_template, request
import requests
import random
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
# change to socket # of partner's micro***
socket.connect("tcp://127.0.0.1:5555")


def generate_random_numbers():
    socket.send_string("generate_numbers")
    response = socket.recv_json()
    return response["num1"], response["num2"]


# Initialize chars_dict, movies_dict, and quotes_list
chars_dict = {}
movies_dict = {}
quotes_list = []


def initialize_dicts():
    global chars_dict, movies_dict, quotes_list, chars_list
    api_endpoint1 = 'https://the-one-api.dev/v2/character'
    api_endpoint_movies = 'https://the-one-api.dev/v2/movie'
    headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}

    # Compile chars_dict {'Char_name1': '_charID1', etc..}
    response1 = requests.get(api_endpoint1, headers=headers)
    data1 = response1.json()
    chars_list = data1['docs']
    for i in range(933):
        char_obj = data1['docs'][i]
        specific_char = data1['docs'][i]['name']
        chars_dict[specific_char] = char_obj['_id']

    # Compile movies_dict {'Movie_name1': '_movieID1', etc..}
    response2 = requests.get(api_endpoint_movies, headers=headers)
    data2 = response2.json()
    movies_dict = {}
    for i in range(2, 8):
        movie = data2['docs'][i]
        specific_movie = data2['docs'][i]['name']
        movies_dict[specific_movie] = movie['_id']

    # Initialize quotes_list (list of quote objects)
    response3_page1 = requests.get('https://the-one-api.dev/v2/quote?page=1',
                                   headers=headers)
    response3_page2 = requests.get('https://the-one-api.dev/v2/quote?page=2',
                                   headers=headers)
    response3_page3 = requests.get('https://the-one-api.dev/v2/quote?page=3',
                                   headers=headers)

    data3_page1 = response3_page1.json()
    data3_page2 = response3_page2.json()
    data3_page3 = response3_page3.json()

    quotes_list = data3_page1['docs']
    quotes_list += data3_page2['docs']
    quotes_list += data3_page3['docs']


# Call the function to initialize both dictionaries when the app starts
initialize_dicts()


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    global chars_dict, movies_dict, quotes_list, chars_list

    cleared = ''

    if request.method == 'POST':
        # num1, page_num, num2 = generate_random_numbers()
        num1 = random.randint(1, 933)
        num2 = random.randint(1, 2384)

        # Getting character info
        # Take care of fields that have 'NaN' or '' to read 'Unknown'
        character = chars_list[num1]
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

        # Use the global chars_dict and movies_dict to display movie name
        # and character name for each quote, instead of movie_id and char_id
        quote = quotes_list[num2]
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
            return render_template('index.html', text=quote_string)
        else:
            return render_template('index.html', text=cleared)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
