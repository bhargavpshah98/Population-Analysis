import sqlite3
import concurrent.futures

def execute_query(query, params=None):
    # Create a new SQLite connection and cursor for each thread
    conn = sqlite3.connect('population_data.db')
    cursor = conn.cursor()

    try:
        if params is not None:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error executing query: {query}\n{e}")
        return None
    finally:
        cursor.close()
        conn.close()

# Function to analyze data in SQLite database
def analyze_data(n):
    queries = [
        '''
        SELECT state, MAX(population) - MIN(population) AS population_increase
        FROM population
        GROUP BY state
        ORDER BY population_increase DESC
        LIMIT :n;
        ''',
        '''
        SELECT state, MAX(population) - MIN(population) AS population_increase
        FROM population
        GROUP BY state
        ORDER BY population_increase ASC
        LIMIT :n;
        '''
        # Add more queries as needed
    ]

    if queries is None or not isinstance(queries, (list, tuple)):
        print("Error: Invalid value for 'queries'. It must be a list or tuple.")
        return

    # Concurrently execute SQL queries
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Pass parameters for each query
        query_params = [{'n': n}, {'n': n}]

        # Map each query with its corresponding parameters
        query_results = executor.map(execute_query, queries, query_params)

        # Pretty print the results
        for i, result_set in enumerate(query_results, 1):
            if result_set is None:
                print(f"Result {i}: No result (query failed)")
            else:
                for j, result in enumerate(result_set, 1):
                    print(f"Result {i}, Subresult {j}: {result}")

if __name__ == "__main__":
    import sys

    # Default value for "n"
    n = 5

    # Check if command line argument is provided for "n"
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            print("Invalid argument for 'n'. Using default value.")

    # Analyze data with the specified number of top states
    analyze_data(n)