import asyncio
import aiohttp
import sqlite3

# API Endpoint
api_url = "https://datausa.io/api/data?drilldowns=State&measures=Population&year=2013,2014,2015,2016,2017,2018,2019,2020,2021"

# Function to create the table
def create_table():
    conn = sqlite3.connect('population_data.db')
    cursor = conn.cursor()

    with open('Data/create_table.sql', 'r') as sql_file:
        create_table_query = sql_file.read()

    cursor.execute(create_table_query)
    conn.commit()

    conn.close()

# Function to insert data into SQLite database
def insert_data_into_sqlite(data):
    if not data or 'data' not in data or not isinstance(data['data'], list):
        print("No valid data to insert into the database.")
        return

    conn = sqlite3.connect('population_data.db')
    cursor = conn.cursor()

    for record in data['data']:
        if isinstance(record, dict) and all(key in record for key in ['State', 'Year', 'Population']):
            state = record['State']
            year = record['Year']
            population = record['Population']

            # Check if the record already exists
            cursor.execute("SELECT COUNT(*) FROM population WHERE state = ? AND year = ?;", (state, year))
            count = cursor.fetchone()[0]

            if count == 0:
                # Insert the record if it doesn't exist
                cursor.execute("INSERT INTO population (state, year, population) VALUES (?, ?, ?);", (state, year, population))
            else:
                print(f"Record for {state} and {year} already exists. Skipping insertion.")
        else:
            print(f"Warning: Unexpected record format. Skipping record: {record}")

    conn.commit()
    print("Data inserted into the database successfully.")

    conn.close()

async def fetch_data(session, url):
    async with session.get(url) as response:
        return await response.json()

async def main():
    async with aiohttp.ClientSession() as session:
        # Create the table
        create_table()

        tasks = []
        # Number of concurrent requests
        num_requests = 10

        for _ in range(num_requests):
            tasks.append(fetch_data(session, api_url))

        api_responses = await asyncio.gather(*tasks)

        # Handle responses for 2022 and 2023
        # (Assuming the API returns empty arrays for these years)
        for api_data in api_responses:
            if not api_data or 'data' not in api_data or not api_data['data']:
                print("No data returned for 2022 and 2023. Handling these cases as needed.")
                continue

            # Insert data into SQLite
            insert_data_into_sqlite(api_data)

if __name__ == "__main__":
    asyncio.run(main())