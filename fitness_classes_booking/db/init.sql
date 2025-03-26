-- Create a database if it doesn’t exist
CREATE DATABASE fitness_db;

-- Create a user if it doesn’t exist
CREATE USE muli WITH ENCRYPTED PASSWORD '15121muli';

-- Grant privileges to the user on the database
GRANT ALL PRIVILEGES ON DATABASE fitness_db TO muli;

-- Allow the user to create schemas and extensions if needed
ALTER DATABASE fitnesss_db OWNER TO muli;
