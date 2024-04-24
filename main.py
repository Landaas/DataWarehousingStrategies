from flask import Flask, jsonify
from pymongo import MongoClient
import psycopg2
from neo4j import GraphDatabase
from bson.json_util import dumps, loads

import os
from pymongo import MongoClient


app = Flask(__name__)

# MongoDB connection
mongo_uri = os.getenv('MONGO_URI', 'mongodb://admin:password@localhost:27017/')
mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client['pokeapi_datawarehouse']

"""# PostgreSQL connection
postgres_conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='pokedw',
    user='admin',
    password='password'
)"""



# Neo4j connection
neo4j_auth = os.getenv('NEO4J_AUTH', 'neo4j/password')
username, password = neo4j_auth.split('/')
neo4j_driver = GraphDatabase.driver('bolt://neo4j:7687', auth=(username, password))



@app.route('/mongodb/<collection_name>', methods=['GET'])
def get_spes_data_from_mongodb(collection_name):
    name = collection_name.capitalize()
    print(name)
    collection = mongo_db[name]
    print(collection)
    data = collection.find()
    return jsonify(dumps(data))
    

"""@app.route('/postgresql', methods=['GET'])
def get_data_from_postgresql():
    cursor = postgres_conn.cursor()
    cursor.execute('SELECT * FROM your_postgresql_table')
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data)"""

@app.route('/neo4j', methods=['GET'])
def get_data_from_neo4j():
    with neo4j_driver.session() as session:
        result = session.run('MATCH (n) RETURN n')
        data = [record['n'] for record in result]
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)