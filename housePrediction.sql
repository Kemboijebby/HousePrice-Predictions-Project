DROP DATABASE IF EXISTS housePrediction;

CREATE DATABASE IF NOT EXISTS housePrediction;

USE housePrediction;

CREATE TABLE IF NOT EXISTS locations (
    id INT NOT NULL AUTO_INCREMENT,
    location VARCHAR(256) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

INSERT INTO locations (location) VALUES ("Kileleshwa"),
    ("Kitisuru"),
    ("Kawangware"),
    ("Runda");