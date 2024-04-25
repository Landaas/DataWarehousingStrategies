from create_postgres_dw import createPostgres
from populate_postgres_dw import loadPostgres
from db_create import create_mongodb

print("Creating Postgres DB")
createPostgres()
print("Loading Postgres DB")
loadPostgres()
print("Postgres Loaded!")
print("Loading MongoDB")
create_mongodb()
print("Loaded MongoDB!")