from pymongo import MongoClient
import requests


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://admin:password@mongo:27017/"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database name as used in the mongodb atlas cloud service)
    return client['pokeapi_datawarehouse']


def fetch_pokemon_data(limit=100):
    url = f'https://pokeapi.co/api/v2/pokemon?limit={limit}'
    response = requests.get(url)
    return response.json()['results']  # Simplified: returns a list of pokemon data


def insert_data(db, data):
    collection_name = db["pokemons"]
    collection_name.insert_many(data)


def main():
    db = get_database()
    pokemon_data = fetch_pokemon_data(limit=100)  # You can adjust the limit or implement pagination
    print(pokemon_data)
    insert_data(db, pokemon_data)
    
if __name__ == "__main__":
    main()
