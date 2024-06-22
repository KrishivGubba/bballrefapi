#This file contains all the currently developed endoints.
#imports:
from flask import Flask, redirect, request, render_template, session, jsonify
from Player import Player
from Team import TeamScraper
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import psycopg2
import os
from dotenv import load_dotenv

#initializing the flask app.
app = Flask(__name__)

#creating a rate limiter that will throttle api requests:
limiter = Limiter(
    get_remote_address,
    app =app,
    default_limits = ["1 per 5 seconds"]
)

load_dotenv

db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_port = os.getenv('DB_PORT')


# creating the table on postgres:
conn = psycopg2.connect(host = db_host, dbname = db_name, user=db_user, password = db_password, port= db_port)
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS playerdetails (
    Career_3FG_Percent DECIMAL(4, 1) DEFAULT 0.0,
    Career_APG DECIMAL(3, 1) DEFAULT 0.0,
    Career_FG_Percent DECIMAL(4, 1) DEFAULT 0.0,
    Career_FT_Percent DECIMAL(4, 1) DEFAULT 0.0,
    Career_Games INT DEFAULT 0,
    Career_PPG DECIMAL(4, 1) DEFAULT 0.0,
    Career_RPG DECIMAL(3, 1) DEFAULT 0.0,
    College VARCHAR(50) DEFAULT 'NA',
    Color VARCHAR(7) DEFAULT '#FFFFFF',
    Experience VARCHAR(20) DEFAULT '0 years',
    HS VARCHAR(50) DEFAULT 'Unknown',
    Image VARCHAR(255) DEFAULT 'https://www.example.com/default.jpg',
    Name VARCHAR(50) DEFAULT 'Unknown',
    Position VARCHAR(100) DEFAULT 'Unknown',
    Season_3FG_Percent DECIMAL(4, 1) DEFAULT 0.0,
    Season_APG DECIMAL(3, 1) DEFAULT 0.0,
    Season_FG_Percent DECIMAL(4, 1) DEFAULT 0.0,
    Season_FT_Percent DECIMAL(4, 1) DEFAULT 0.0,
    Season_Games INT DEFAULT 0,
    Season_PPG DECIMAL(4, 1) DEFAULT 0.0,
    Season_RPG DECIMAL(3, 1) DEFAULT 0.0,
    Shooting_arm VARCHAR(5) DEFAULT 'Unknown'
);
''')
cur.execute('''CREATE TABLE IF NOT EXISTS team_players (
    id SERIAL PRIMARY KEY,
    player_name VARCHAR(100),
    position VARCHAR(50),
    team_code VARCHAR(10),
    year INT
);
''')
conn.commit()
cur.close()
conn.close()

#first endpoint fetches a player's profile
@app.route("/api/player-stats", methods = ["GET"])
@limiter.limit("1 per 5 seconds") #rate limiting
def getPlayerStats():
    #adhering to RESTful standards by rejecting requests with payload.
    if request.data: return {"Error":"GET request should not have a request body."}, 400

    player_name = request.args.get("name").lower()
    #checking to see that the player's name has been provided as req param.
    if not player_name:
        return {"Error": "Provide a player name as a request parameter"}, 400
    #first we will check to see if the database already has the table or not.
    conn = psycopg2.connect(
        host = db_host, dbname = db_name, user=db_user, password = db_password, port= db_port
    )
    cur = conn.cursor()
    #now construct query to check if this player exists within the database.
    query = "SELECT * FROM playerdetails WHERE LOWER(Name) = %s LIMIT 1;"
    cur.execute(query, (player_name,))
    # Fetch the result
    result = cur.fetchone()
    if not result: #in case the database does not hold the required player's data.
        try:
            playerObject = Player(playername=player_name)
        except:
            return jsonify("Error : player was not found.") , 404
        player_details = playerObject.playerProfile() #attempting to scrape the data
        values = (
        player_details['Career 3FG%'],
        player_details['Career APG'],
        player_details['Career FG%'],
        player_details['Career FT%'],
        player_details['Career Games'],
        player_details['Career PPG'],
        player_details['Career RPG'],
        player_details['College'],
        player_details['TeamColor'],
        player_details['Experience'],
        player_details['HS'],
        player_details['Image'],
        player_details['Name'],
        player_details['Position'],
        player_details['Season 3FG%'],
        player_details['Season APG'],
        player_details['Season FG%'],
        player_details['Season FT%'],
        player_details['Season Games'],
        player_details['Season PPG'],
        player_details['Season RPG'],
        player_details['Shooting arm']
    )

        # Construct the SQL INSERT statement
        insert_query = """
        INSERT INTO playerdetails (
            Career_3FG_Percent, Career_APG, Career_FG_Percent, Career_FT_Percent,
            Career_Games, Career_PPG, Career_RPG, College, Color, Experience, HS,
            Image, Name, Position, Season_3FG_Percent, Season_APG, Season_FG_Percent,
            Season_FT_Percent, Season_Games, Season_PPG, Season_RPG, Shooting_arm
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(insert_query, values)
        conn.commit()
        conn.close()
        
        return jsonify(player_details), 200
    else:# in the case of the player's data existing within the dbase.
        values = result
        result_keys = ['Career 3FG%', 'Career APG', 'Career FG%', 'Career FT%', 'Career Games', 'Career PPG', 
                       'Career RPG', 'College', 'TeamColor', 'Experience', 'HS', 'Image', 'Name', 'Position', 'Season 3FG%', 
                       'Season APG', 'Season FG%', 'Season FT%', 'Season Games', 'Season PPG', 'Season RPG', 'Shooting arm']
        res = {}
        for i in range(len(result_keys)):
            res[result_keys[i]] = values[i] if values[i] else "NA"

        return jsonify(res), 200

#returns the whole roster for a team for a particular year.
@app.route("/api/team-year-roster")
@limiter.limit("1 per 5 seconds") #rate limiting
def getRoster():
    if request.data: return {"Error":"GET request should not have a request body."}, 400
    team_code = request.args.get("team")
    year = request.args.get("year")
    if not team_code or not year: #checking to see that the query params of the GET request is properly formatted
        return {"Error": "Provide a team code and year in the query parameters"}, 400
    #connecting to the dbase
    conn = psycopg2.connect(
        host = db_host, dbname = db_name, user=db_user, password = db_password, port= db_port
    )
    # Create a cursor object
    cur = conn.cursor()
    # Define the query
    query = '''
    SELECT player_name, position
    FROM team_players
    WHERE team_code = %s AND year = %s;
    '''
    # Execute the query
    cur.execute(query, (team_code, year))
    # Fetch all results
    results = cur.fetchall()
    # Close the cursor and connection

    if not results: #in case the data does not exist within our database.
        teamscraper = TeamScraper(teamcode=team_code)
        results = teamscraper.getRoster(int(year))
        if not results:
            return {"Error" : "Could not find queried data."}
        #now must add the results to the sql dbase.
        insert_query = '''
            INSERT INTO team_players (player_name, position, team_code, year)
            VALUES (%s, %s, %s, %s);
        '''
        for player_name, position in results.items():
            cur.execute(insert_query, (player_name, position, team_code, year))
        conn.commit()
        cur.close()
        conn.close()
        print("these are the res", results)
        return jsonify(results), 200
    else: # in case the data is within the dbase.
        returnable = {}
        for i in range(len(results)):
            returnable[results[i][0]] = results[i][1]
        return jsonify(returnable)


@app.route("/api/player-prev-games")
@limiter.limit("1 per 5 seconds") #providing the rate limit.
def getLastFewGames():
    data = request.json
    #checking to see that the request body isformatted properly
    if not data or "name" not in data:
        return {"Error":"Reformat the request body"}, 400
    playerName = data['name']
    #creating a player object to start scraping the stats
    player = Player(playerName)
    try:
        games = player.lastFewGames()
        return jsonify(games)
    except:
        return {"Error" : "An error occurred while scraping data."}

if __name__=="__main__":
    app.run(debug=True)