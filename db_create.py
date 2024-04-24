from pymongo import MongoClient
import requests
import time
import csv
from ranges import ranges

def get_database():
    """Establish a connection to the MongoDB database."""
    CONNECTION_STRING = "mongodb://admin:password@mongo:27017/"
    client = MongoClient(CONNECTION_STRING)
    return client['pokeapi_datawarehouse']

def fetch_pokemon_data(url, data_points):
    """Fetch data from the PokeAPI and extract required data points."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        json_response = response.json()
        return {data_point: json_response.get(data_point) for data_point in data_points}
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def insert_data(collection, data):
    """Insert multiple documents into a MongoDB collection."""
    if data:
        collection.insert_many(data)



def getPokemon():
    db = get_database()
    print(db)
    pokemon_collection = db['pokemons']
    limit = 0
    next_url = f'https://pokeapi.co/api/v2/pokemon?limit={1}'
    data_store = []

    while limit < ranges[1]:    
        data = fetch_pokemon_data(next_url, ['next', 'results'])
        if not data:
            break  # Exit the loop if no data is fetched
        
        pokemon_entries = data['results']
        next_url = data['next']  # Update the next URL

        for pokemon in pokemon_entries:
            print(pokemon['name'])
            info = fetch_pokemon_data(pokemon['url'], ['id', 'moves', 'stats', 'types'])
            if info:
                pokemon.update({
                    'pokemon_id': info['id'],
                    'types': info['types'],
                    'moves': [move for move in info['moves'] if move.get('version_group_details')],
                    **{f"base_{stat['stat']['name']}": stat['base_stat'] for stat in info['stats'] if stat['stat']['name'] in ['hp', 'attack', 'defense', 'speed']}
                })
                data_store.append(pokemon)
        
        if data_store:
            insert_data(pokemon_collection, data_store)
            data_store = []  # Clear the list after inserting to database

        limit += 1

def getmoves():
    db = get_database()
    pokemon_collection = db['moves']
    data_store = []
    limit = 1
    
    while limit < ranges[3] + 1:    
        data = fetch_pokemon_data(f'https://pokeapi.co/api/v2/move/{limit}/', ['name', 'type','power','pp','accuracy'])
        if not data:
            break  # Exit the loop if no data is fetched

        data.update({'move_id':limit})
        limit += 1  # Update the next URL
        data_store.append(data)
        print(data_store)

        if data_store:
                insert_data(pokemon_collection, data_store)
                data_store = []  # Clear the list after inserting to database

        time.sleep(1)  # Throttle API requests to avoid rate limits




    
def gettypes():
    db = get_database()
    pokemon_collection = db['types']
    data_store = []
    limit = 1
    
    while limit < 10:    
        data = fetch_pokemon_data(f'https://pokeapi.co/api/v2/type/{limit}/', ['name'])
        if not data:
            break  # Exit the loop if no data is fetched

        data.update({'type_id':limit})
        limit += 1  # Update the next URL
        data_store.append(data)
        print(data_store)

        if data_store:
                insert_data(pokemon_collection, data_store)
                data_store = []  # Clear the list after inserting to database

        time.sleep(1)  # Throttle API requests to avoid rate limits
    
def getlocations():
    db = get_database()
    pokemon_collection = db['locations']
    data_store = []
    limit = 1
    
    while limit < ranges[0]:    
        data = fetch_pokemon_data(f'https://pokeapi.co/api/v2/location/{limit}/', ['name'])
        if not data:
            break  # Exit the loop if no data is fetched

        data.update({'location_id':limit})
        limit += 1  # Update the next URL
        data_store.append(data)
        print(data_store)

        if data_store:
                insert_data(pokemon_collection, data_store)
                data_store = []  # Clear the list after inserting to database

        time.sleep(1)  # Throttle API requests to avoid rate limits



def read_csv_to_dict_list(file_path):
    # Define the keys for the dictionary
    keys = ['Location', 'winner pokemon', 'losing pokemon', 'Winning move', 'Duration','Losing move', 'date']
    data_list = []
    
    # Open the CSV file and read each line into a dictionary using the predefined keys
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Make sure the row has exactly the number of elements expected (6 in this case)
            if len(row) == len(keys):
                data_dict = dict(zip(keys, row))
                data_list.append(data_dict)
            else:
                print("Error: Row does not match expected format")
    
    return data_list

def getBattles():
    db = get_database()
    pokemon_collection = db['Battles']
    data = read_csv_to_dict_list('dataset.csv')
    insert_data(pokemon_collection, data)


def create_mongodb():
    getPokemon()
    getmoves()
    gettypes()
    getlocations()
    getBattles()

if __name__ == "__main__":
    create_mongodb()
