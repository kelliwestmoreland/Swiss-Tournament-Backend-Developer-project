-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament; -- removes old database (if applicable)
CREATE DATABASE tournament; -- adds new tournament database

\c tournament -- connects to tournament database

CREATE TABLE players (id SERIAL primary key, 
					name TEXT);
); /*id for the match, which will also be a primary key, and the name in text form*/

CREATE TABLE matches (id SERIAL primary key, 
					winner INTEGER REFERENCES players (id), 
					loser INTEGER REFERENCES players (id));
); /*id for players as a primary key, the winner, then loser in integer form and references the players table and id*/


CREATE VIEW standings AS 
SELECT players.id as id, name,
	(SELECT count(*) FROM matches WHERE matches.winner = players.id ) AS winners,
	(SELECT count(*) FROM matches WHERE players.id in (winner,loser)) AS matches_played
		FROM players
		GROUP by players.id
		ORDER by winners DESC
; /*views created with subqueries to create 4 columns for ids, name, winners, and total matches played
will call the view with 'standings'*/

