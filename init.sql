
-- Datu basea sortu
CREATE DATABASE IF NOT EXISTS mbtidb;

-- Baimenak eman
GRANT ALL PRIVILEGES ON mbtidb.* TO 'user'@'%' IDENTIFIED BY 'pass' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root' WITH GRANT OPTION;

FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS mbti_labels (
    id BIGINT PRIMARY KEY,
    mbti_personality VARCHAR(10),
    pers_id INT
);




LOAD DATA INFILE '/data/mbti_labels.csv'
INTO TABLE mbti_labels
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, mbti_personality,pers_id);

