# Population Data Analysis

## Introduction

This project fetches population data from an API, stores it in an SQLite database, and performs analysis on the data. The analysis includes queries to find population increases and decreases for different states.

## Features

- Fetches population data from an API concurrently
- Stores data in an SQLite database in asynchronous manner
- Performs analysis on population data with user input

## Getting Started

### Prerequisites

- Python 3.x
- Requests library (`pip install requests`)
- asyncio library (`pip install asyncio`)
- sqlite3 library (`pip install sqlite3`)
- concurrent.futures (`pip install concurrent.futures`)
- aiohttp library (`pip install aiohttp`)

### Installation

1. Clone the repository:

   ```bash
   git clone `https://github.com/bhargavpshah98/Population-Analysis.git`
   cd Population-Analysis

2. Install all the Prerequisites

   Follow the commands given in the prerequisites

3. First run the fetch_and_store.py file to load the data into the database

   python3 scripts/fetch_and_store.py  

4. Then run the analyze_data.py file to analyze the data and give and number as input for it

   python3 scripts/analyze_data.py <your_input>

   If you don't enter the input, it will automatically take 5 as an input

You will be able to see the output in the command line
