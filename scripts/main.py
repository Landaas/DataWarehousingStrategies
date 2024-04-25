from flask import Flask, jsonify, request
from pymongo import MongoClient
import psycopg2
from neo4j import GraphDatabase
from bson.json_util import dumps, loads
from py2neo import Graph


import os
from pymongo import MongoClient


app = Flask(__name__)

# MongoDB connection
mongo_uri = os.getenv('MONGO_URI', 'mongodb://admin:password@host.docker.internal:27017/')
mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client['pokeapi_datawarehouse']

def connectPostgres():
    try: 
        postgres_conn = psycopg2.connect(
            host="host.docker.internal",
            user='admin',
            password='password',
            dbname='pokedw'
        )
        return postgres_conn
    except psycopg2.Error as e: 
        print("Error connecting to PostgreSQL server:", e)
        return None
    
# PostgreSQL connection

# Neo4j connection
neo4j_auth = os.getenv('NEO4J_AUTH', 'neo4j/password')
username, password = neo4j_auth.split('/')
#neo4j_driver = Graph.driver('bolt://host.docker.internal:7687', auth=(username, password))




@app.route('/mongodb/<collection_name>', methods=['GET'])
def get_spes_data_from_mongodb(collection_name):
    name = collection_name
    print(name)
    collection = mongo_db[name]
    print(collection)
    data = collection.find()
    return jsonify(dumps(data))

@app.route('/mongodb', methods=['POST'])
def query_mongodb():
    content = request.json
    print(content)
    name = content["collection"]
    print(name)
    collection = mongo_db[name]
    print(content["query"])
    data = collection.find({"move_id": "1"}) if "query" in content and content["query"] else collection.find()
    return jsonify(dumps(data))
    

@app.route('/postgresql', methods=['POST'])
def query_postgres():
    content = request.json
    postgres_conn = connectPostgres()
    if not postgres_conn: return 'Unable to connect to Postgres Server!', 500
    if content:
        cursor = postgres_conn.cursor()
        cursor.execute(content)
        data = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
        cursor.close()
        return jsonify({"headers": colnames, "results": data})
    else:
        return 'bad request!', 400

@app.route('/neo4jbuild', methods=['GET'])
def get_data_from_neo4j():
    graph = Graph('bolt://host.docker.internal:7687', auth=(username, password))
    i = 1
    with open("./all.cypher", "r") as f:
        cypher_query = f.read().strip()
        for line in cypher_query.split("\n"):
            if line.find(":begin") >= 0:
                pass
            elif line.find(":commit") >= 0:
                graph.commit()
            else: 
                graph.run(line)
            i += 1

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)