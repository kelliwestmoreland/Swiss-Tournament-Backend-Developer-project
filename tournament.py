#/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2



def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    db = connect() #connect to database
    db_cursor = db.cursor() #create a cursor to execute the command
    query = "DELETE FROM matches;" #SQL query with what the action will be, this one is deleting
    db_cursor.execute(query)#the line to execute the query
    db.commit() #must commit to execute the delete action
    db.close() #close the connection

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect() #connect to database
    db_cursor = db.cursor()
    query = "DELETE FROM players;"
    db_cursor.execute(query)
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect() #connect to database
    db_cursor = db.cursor() #added in to connect to database and execute cursor
    query = "SELECT COUNT(id) AS num from players"; #using id as way to count players
    db_cursor.execute(query) #added in to execute query
    results = db_cursor.fetchone() #returns players by one line
    db.close() 
    if results:
    	return results[0] #returns count of players registered
    else:
    	return '0' #returns zero if no players are registered

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect() #connect to database
    db_cursor = db.cursor() #using cursor object to execute next command
    query = "INSERT INTO players(name) VALUES('%s');" % name #we want to pass name in % name as a string %s
    db_cursor.execute("INSERT INTO players(name) VALUES(%s)", (name,)) #will execute query to register players
    db.commit() #commit to execut the insert function
    db.close() #close database connection

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    standings = [] #standings will be called in python
    db = connect() #connect to database
    db_cursor = db.cursor() #using cursor object to execute the query (which was created within views/subquery within views)
    query = "SELECT * FROM standings;" #calls views in sql to create columns for id, name, winners, and total matches played
    db_cursor.execute(query) #will execute query for standings
    standings = db_cursor.fetchall() #returns all the standings to evaluate
    #python used to evaluate the standings
    for row in db_cursor.fetchall(): 
        for player in standings in zip(id, player, winner, matches): #zip used to iterate through the list of standings, referenced https://stackoverflow.com/questions/13704860/zip-lists-in-python
            standings.append((row[0], str(row[1]), row[2], row[3])) #returns tuples of id, name, wins, matches

    db.close() #closes database
    return standings #returns standings from playerStandings()

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect() #connects to database
    db_cursor = db.cursor() #using cursor object to execute the upcoming query
    sql = "INSERT into matches (winner, loser) VALUES (%s, %s)" #executes outcome of single match between two players
    data = (winner, loser) # added in data, removed string to prevent SQL injection
    db_cursor.execute(sql, data)
    db.commit() #will save the winner, loser inserted
    db.close() #closes connection to database

 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings() #calls playerStandings to return list of players to evaluate for next rounds
    #reviewed len/while loop https://www.khanacademy.org/computing/computer-programming/programming/looping/p/intro-to-while-loops https://nedbatchelder.com/text/iter.html
    i = 0 
    result = []
    #while loop to review entire list of standings, create new pairs, making sure each player exists once in pairings
    while i < len(standings) - 1: 
        result.append((standings[i][0], standings[i][1], standings[i + 1][0], standings[i + 1][1])) #append list of results of tuples of id1, name1, id2, name2
        i += 2
    return result #returns list of pairs of registered players 
