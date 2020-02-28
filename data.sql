-- $ sqlite3 data.db < data.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS  data;
CREATE TABLE posts (
    id INTEGER primary key,
    community VARCHAR,
    title VARCHAR,
    description VARCHAR,
    published INTEGER,
    visibility INTEGER,
    username VARCHAR,
    votes_id INTEGER,
    UNIQUE(id)
);
INSERT INTO posts(id, community, title, description, published, visibility, username, votes_id) VALUES(1, 'TEST_Sub', 'Demo post', 'A demo post description', 2020, 1, 'nobody', 10001);
CREATE TABLE votes (
    votes_id INTEGER primary key,
    upvotes INTEGER,
    downvotes INTEGER,
    UNIQUE(votes_id)
);
INSERT INTO votes(votes_id, upvotes, downvotes) VALUES(10001, 100, 25);
COMMIT;
