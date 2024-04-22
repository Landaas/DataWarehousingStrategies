from pymongo import MongoClient
import requests
import time

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

def main():
    db = get_database()
    pokemon_collection = db['pokemons']
    
    limit = 10
    next_url = f'https://pokeapi.co/api/v2/pokemon?limit={limit}'
    data_store = []

    while next_url:    
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
                    'id': info['id'],
                    'types': info['types'],
                    'moves': [move for move in info['moves'] if move.get('version_group_details')],
                    **{f"base_{stat['stat']['name']}": stat['base_stat'] for stat in info['stats'] if stat['stat']['name'] in ['hp', 'attack', 'defense', 'speed']}
                })
                data_store.append(pokemon)
        
        if data_store:
            insert_data(pokemon_collection, data_store)
            data_store = []  # Clear the list after inserting to database

        time.sleep(1)  # Throttle API requests to avoid rate limits

if __name__ == "__main__":
    main()
