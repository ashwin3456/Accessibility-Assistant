-- Create database
CREATE DATABASE IF NOT EXISTS accessibility_assistant;
USE accessibility_assistant;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    disability VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data (optional)
-- INSERT INTO users (name, email, password, disability) VALUES 
-- ('Test User', 'test@example.com', 'hashed_password', 'visual_impairment');
