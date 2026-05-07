-- FinGuard AI Database Setup
-- Run this in pgAdmin or psql

-- Create database
CREATE DATABASE finguard_db;

-- Create user
CREATE USER finguard_user WITH PASSWORD 'finguard_pass';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE finguard_db TO finguard_user;

-- Connect to the database
\c finguard_db

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO finguard_user;

-- Verify
SELECT datname FROM pg_database WHERE datname = 'finguard_db';
