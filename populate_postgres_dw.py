from pymongo import MongoClient
import requests
import time
import psycopg2
from ranges import ranges


def connect_to_postgres(user, password, dbname):
    try:
        conn = psycopg2.connect(
            user=user,
            password=password,
            dbname=dbname
        )
        print("Connected to PostgreSQL server")
        return conn
    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL server:", e)
        return None

def fetch_pokemon_data(url):
    """Fetch data from the PokeAPI and extract required data points."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def get_database():
    pass

def getPokemon(conn):
    cur = conn.cursor()
    url = f'https://pokeapi.co/api/v2/pokemon?limit={ranges[1]}'
    data = fetch_pokemon_data(url)
    for pk in data['results']:
        pokedata = fetch_pokemon_data(pk['url'])
        pokemon = (
            pokedata['id'],
            pokedata['name'],
            pokedata['types'][0]['type']['name'],
            pokedata['types'][1]['type']['name'] if len(pokedata['types']) > 1 else 'NULL',
            pokedata['stats'][0]['base_stat'],
            pokedata['stats'][1]['base_stat'],
            pokedata['stats'][2]['base_stat'],
            pokedata['stats'][5]['base_stat']
            )
        cur.execute("""
                    INSERT INTO pokemon (pid, pname, ptype_primary, ptype_secondary, pbase_hp, pbase_attack, pbase_defence, pbase_speed) 
                    VALUES (%s,'%s','%s','%s',%s,%s,%s,%s);
                    """ % pokemon)
    print("Added pokemon")

def getBattles(conn):
    cur = conn.cursor()
    with open("dataset.csv", 'r') as f:
        for line in f.readlines():
            data = line[:-1]
            values = data.split(',')
            cur.execute("""
                INSERT INTO battles (lid, winner_pid, loser_pid, winning_mid, losing_mid, bduration, bdate) 
                VALUES (%s,%s,%s,%s,%s,%s,'%s');
                """ % tuple(values))
    print("Added all battles")

def getmoves(conn):
    cur = conn.cursor()
    data = fetch_pokemon_data(f'https://pokeapi.co/api/v2/move?limit={ranges[3]}')
    
    for mov in data['results']:   
        movedata = fetch_pokemon_data(mov['url'])
        move = (
            movedata['id'],
            movedata['name'],
            movedata['type']['name'],
            movedata['power'] if movedata['power'] else 'NULL',
            movedata['pp'] if movedata['accuracy'] else 'NULL',
            movedata['accuracy'] if movedata['accuracy'] else 'NULL',
            )
        cur.execute("""
                    INSERT INTO moves (mid, mname, mtype, mpower, mpp, maccuracy) 
                    VALUES (%s,'%s','%s',%s,%s,%s);
                    """ % move)
    print("Added moves")
    
def getlocations(conn):
    cur = conn.cursor()
    data = fetch_pokemon_data(f'https://pokeapi.co/api/v2/location?limit={ranges[0]}')
    
    for i, loc in enumerate(data['results']):   
        location = (
            i,
            loc['name']
            )
        cur.execute("""
                    INSERT INTO locations (lid, lname) 
                    VALUES (%s,'%s');
                    """ % location)
    print("Added locations")


def main():
    # PostgreSQL server details
    user = "admin"
    password = "password"
    dbname = "pokedw"

    # Connect to PostgreSQL server
    conn = connect_to_postgres(user, password, dbname)
    if conn is None:
        return
    getPokemon(conn)
    getBattles(conn)
    getmoves(conn)
    getlocations(conn)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
