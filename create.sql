
-- DROP TABLES IF THEY EXIST
DROP TABLE IF EXISTS episode_colors;
DROP TABLE IF EXISTS episode_subjects;
DROP TABLE IF EXISTS episodes;
DROP TABLE IF EXISTS colors;
DROP TABLE IF EXISTS subjects;

-- CREATE TABLES

CREATE TABLE episodes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    season INT,
    episode INT,
    air_date DATE,
    image_url TEXT,
    video_url TEXT
);

CREATE TABLE colors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    hex_code VARCHAR(7)
);

CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE episode_colors (
    episode_id INT REFERENCES episodes(id) ON DELETE CASCADE,
    color_id INT REFERENCES colors(id) ON DELETE CASCADE,
    PRIMARY KEY (episode_id, color_id)
);

CREATE TABLE episode_subjects (
    episode_id INT REFERENCES episodes(id) ON DELETE CASCADE,
    subject_id INT REFERENCES subjects(id) ON DELETE CASCADE,
    PRIMARY KEY (episode_id, subject_id)
);
