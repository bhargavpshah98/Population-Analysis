CREATE TABLE IF NOT EXISTS population (
    state TEXT,
    year INTEGER,
    population INTEGER,
    PRIMARY KEY (state, year)
);
