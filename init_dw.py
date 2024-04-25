from create_postgres_dw import createPostgres
from populate_postgres_dw import loadPostgres
from db_create import create_mongodb
from generate_dataset import generateDataset
import asyncio

async def postgres():
    print("Creating Postgres DB")
    createPostgres()
    print("Loading Postgres DB")
    loadPostgres()
    print("Postgres Loaded!")

async def mongodb():
    print("Loading MongoDB")
    create_mongodb()
    print("Loaded MongoDB!")

async def main():
    print("Generating Dataset")
    generateDataset()
    tasks = [
        asyncio.create_task(mongodb()),
        asyncio.create_task(postgres()),
    ]

    await asyncio.wait(tasks)

if __name__ == '__main__':
    asyncio.run(main())
    