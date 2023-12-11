-- Create Database
CREATE DATABASE IF NOT EXISTS fitness_tracker;
USE fitness_tracker;

-- Create Users Table
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL
);

-- Create Goals Table
CREATE TABLE IF NOT EXISTS Goals (
    goal_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    goal_name VARCHAR(100) NOT NULL,
    goal_type VARCHAR(50) NOT NULL,
    goal_target INT NOT NULL,
    progress INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Create Activities Table
CREATE TABLE IF NOT EXISTS Activities (
    activity_id INT AUTO_INCREMENT PRIMARY KEY,
    goal_id INT,
    activity_date DATE NOT NULL,
    activity_value INT NOT NULL,
    FOREIGN KEY (goal_id) REFERENCES Goals(goal_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Create Indexes
CREATE INDEX idx_user_id_goals ON Goals (user_id);
CREATE INDEX idx_goal_id_activities ON Activities (goal_id);

-- Insert Sample Data
INSERT INTO Users (username, password_hash, email) VALUES
('user1', 'hashed_password1', 'user1@example.com'),
('user2', 'hashed_password2', 'user2@example.com');

INSERT INTO Goals (user_id, goal_name, goal_type, goal_target, progress) VALUES
(1, 'Daily Steps', 'steps', 10000, 7500),
(1, 'Weekly Workout', 'hours', 5, 3),
(2, 'Weight Loss', 'lbs', 10, 0);

INSERT INTO Activities (goal_id, activity_date, activity_value) VALUES
(1, '2023-01-01', 8000),
(1, '2023-01-02', 8500),
(2, '2023-01-01', 2),
(2, '2023-01-02', 2),
(3, '2023-01-01', 0);

-- Create User for Flask Application
CREATE USER 'flask_user'@'localhost' IDENTIFIED BY 'password';
GRANT SELECT, INSERT, UPDATE, DELETE ON fitness_tracker.* TO 'flask_user'@'localhost';
FLUSH PRIVILEGES;
