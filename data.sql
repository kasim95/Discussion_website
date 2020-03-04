-- $ sqlite3 data.db < data.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS  data;

CREATE TABLE votes (
    vote_id INTEGER primary key,
    upvotes INTEGER,
    downvotes INTEGER
);

CREATE TABLE community (
    community_id INTEGER primary key,
    name VARCHAR
);

CREATE TABLE posts (
    post_id INTEGER primary key,
    community_id VARCHAR,
    title VARCHAR,
    description VARCHAR,
    published TIMESTAMP DEFAULT (DATETIME('now', 'localtime')),
    username VARCHAR,
    vote_id INTEGER,
    FOREIGN KEY (vote_id) REFERENCES votes (vote_id),
    FOREIGN KEY (community_id) REFERENCES community (community_id)       
);
/*INSERT INTO posts(community, title, description, username) VALUES('TEST_Sub1', 'Demo post1', 'A demo post description1', DATETIME('now','localtime'), 'nobody');
INSERT INTO posts(community, title, description, username) VALUES('TEST_Sub2', 'Demo post2', 'A demo post description2',CURRENT_TIMESTAMP, 'nobody');
*/
INSERT INTO votes(upvotes, downvotes) VALUES(100, 25);
INSERT INTO community(community_id, name) VALUES(1, 'cs');
INSERT INTO posts(community_id, title, description, username, vote_id) VALUES(1, 'Demo post1', 'A demo post description1','nobody',(SELECT MAX(vote_id) from votes));

INSERT INTO votes(upvotes, downvotes) VALUES(99, 24);
INSERT INTO community(community_id, name) VALUES(2, 'hi');
INSERT INTO posts(community_id, title, description, username, vote_id) VALUES(2, 'Demo post2', 'A demo post description2','nobody',(SELECT MAX(vote_id) from votes));

INSERT INTO votes(upvotes, downvotes) VALUES(98, 23);
INSERT INTO posts(community_id, title, description, username, vote_id) VALUES(2, 'Demo post3', 'A demo post description3','nobody',(SELECT MAX(vote_id) from votes));

INSERT INTO votes(upvotes, downvotes) VALUES(97, 22);
INSERT INTO posts(community_id, title, description, username, vote_id) VALUES(1, 'Demo post4', 'A demo post description4','nobody',(SELECT MAX(vote_id) from votes));

COMMIT;
