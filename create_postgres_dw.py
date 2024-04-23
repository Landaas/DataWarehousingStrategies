import psycopg2
from psycopg2 import sql

# Function to connect to PostgreSQL server
def connect_to_postgres(user, password, dbname):
    try:
        conn = psycopg2.connect(
            user=user,
            password=password,
            dbname="postgres"
        )
        conn.autocommit = True
        print("Connected to PostgreSQL server")
        cur = conn.cursor()
        cur.execute("DROP DATABASE " + dbname + " WITH (force)")
        cur.execute("CREATE DATABASE " + dbname)
        conn = psycopg2.connect(
            user=user,
            password=password,
            dbname=dbname
        )
        return conn
    except psycopg2.Error as err:
        print(err)
        try:
            conn = psycopg2.connect(
                user=user,
                password=password,
                dbname="postgres"
            )
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute("CREATE DATABASE " + dbname)
            conn = psycopg2.connect(
                user=user,
                password=password,
                dbname=dbname
            )
            return conn
        except psycopg2.Error as e: 
            print("Error connecting to PostgreSQL server:", e)
            return None

# Function to create a new table
def create_tables(conn):
    try:
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS battles (
                bid SERIAL PRIMARY KEY,
                lid INT,
                winner_pid INT,
                loser_pid INT,
                winning_mid INT,
                losing_mid INT,
                bduration INT,
                bdate DATE
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pokemon (
                pid INT PRIMARY KEY,
                pname VARCHAR(100),
                ptype_primary VARCHAR(20),
                ptype_secondary VARCHAR(20),
                pbase_hp INT,
                pbase_attack INT,
                pbase_defence INT,
                pbase_speed INT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS moves (
                mid INT PRIMARY KEY,
                mname VARCHAR(100),
                mtype VARCHAR(20),
                mpower INT,
                mpp INT,
                maccuracy NUMERIC
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS locations (
                lid INT PRIMARY KEY,
                lname VARCHAR(150)
            )
        """)
        print("Tables created successfully")
        cur.close()
    except psycopg2.Error as e:
        print("Error creating table:", e)

# Main function
def main():
    # PostgreSQL server details
    user = "admin"
    password = "password"
    dbname = "pokedw"

    # Connect to PostgreSQL server
    conn = connect_to_postgres(user, password, dbname)
    if conn is None:
        return

    # Create a new database
    # create_database(conn, "postgres_dw")

    # Connect to the newly created database
    conn.close()  # Close the previous connection
    conn = connect_to_postgres(user, password, dbname)

    # Create a new table in the database
    create_tables(conn)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()
