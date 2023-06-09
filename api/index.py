from flask import Flask, render_template, json, redirect, request
from dotenv import load_dotenv
import os
import psycopg2

app = Flask(__name__)

load_dotenv()
db_user = os.environ.get('DB_USER')
db_pswrd = os.environ.get('DB_PSWRD')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_database = os.environ.get('DB_DATABASE')

# establishing connection to database
def get_db_connection():
    connection = psycopg2.connect(user=db_user,
                                    password=db_pswrd,
                                    host=db_host,
                                    port=db_port,
                                    database=db_database)
    return connection

class Player:
  def __init__(self, row) -> None:
    self.name = row[0]
    self.home_wins = row[1]
    self.home_loses = row[2]
    self.home_ties = row[3]
    self.home_pf = row[4]
    self.home_pa = row[5]
    self.away_wins = row[6]
    self.away_loses = row[7]
    self.away_ties = row[8]
    self.away_pf = row[9]
    self.away_pa = row[10]
    
    pass
  
  @property
  def wins(self):
    return self.home_wins + self.away_wins
  
  @property
  def loses(self):
    return self.home_loses + self.away_loses
  
  @property
  def diff(self):
    return self.home_pf + self.away_pf - self.home_pa - self.away_pa
  
  @property
  def games(self):
    return self.wins + self.loses
  
  @property
  def wp(self):
    if self.games == 0:
      return 0
    print(self.wins, self.games)
    return float(self.wins) / self.games



@app.route('/')
def home():
  
  conn = get_db_connection()
  cursor = conn.cursor()
  
  cursor.execute("""SELECT NAME,

	(SELECT COUNT(*)
		FROM GAMES
		WHERE HOME_PLAYER = NAME
			AND HOME_SCORE > AWAY_SCORE) AS HOME_WINS,

	(SELECT COUNT(*)
		FROM GAMES
		WHERE HOME_PLAYER = NAME
			AND HOME_SCORE < AWAY_SCORE) AS HOME_LOSES,

	(SELECT COUNT(*)
		FROM GAMES
		WHERE HOME_PLAYER = NAME
			AND HOME_SCORE = AWAY_SCORE) AS HOME_TIES,

	(SELECT COALESCE(SUM(HOME_SCORE),

										0)
		FROM GAMES
		WHERE HOME_PLAYER = NAME ) AS HOME_POINTS_FOR,

	(SELECT COALESCE(SUM(AWAY_SCORE),

										0)
		FROM GAMES
		WHERE HOME_PLAYER = NAME ) AS HOME_POINTS_AGAINST,

	(SELECT COUNT(*)
		FROM GAMES
		WHERE AWAY_PLAYER = NAME
			AND HOME_SCORE < AWAY_SCORE) AS AWAY_WINS,

	(SELECT COUNT(*)
		FROM GAMES
		WHERE AWAY_PLAYER = NAME
			AND HOME_SCORE > AWAY_SCORE) AS AWAY_LOSES,

	(SELECT COUNT(*)
		FROM GAMES
		WHERE AWAY_PLAYER = NAME
			AND HOME_SCORE = AWAY_SCORE) AS AWAY_LOSES,

	(SELECT COALESCE(SUM(AWAY_SCORE),

										0)
		FROM GAMES
		WHERE AWAY_PLAYER = NAME ) AS AWAY_POINTS_FOR,

	(SELECT COALESCE(SUM(HOME_SCORE),

										0)
		FROM GAMES
		WHERE AWAY_PLAYER = NAME ) AS AWAY_POINTS_AGAINST
FROM PLAYERS;""")
  players = cursor.fetchall()
  print(cursor.description)
  
  cursor.close()
  conn.close()
  
  players = [Player(row) for row in players]
  players.sort(key= lambda x : (x.loses, x.name))
  players.sort(reverse=True, key = lambda x: (x.wp, x.games, x.diff))
    
  return render_template('index.html', players = players)
  
@app.route('/admin')
def admin():
  return render_template('admin.html')

@app.route('/save')
def save():
  return json.dumps([])

@app.route('/upload', methods=['POST'])
def upload():
  
  
  return redirect('/admin')

@app.route('/newGame', methods=['POST'])
def newGame():
  
  hp = request.form.get('homePlayer')
  awp = request.form.get('awayPlayer')
  hs = request.form.get('homeScore')
  aws = request.form.get('awayScore')
  
  conn = get_db_connection()
  cursor = conn.cursor()
  
  cursor.execute("""INSERT INTO games (home_player, away_player, home_score, away_score) VALUES (%s, %s, %s, %s);""", (hp, awp, hs, aws))
  
  cursor.close()
  conn.commit()
  conn.close() 
  
  return redirect('/admin')

@app.route('/newPlayer', methods=['POST'])
def newPlayer():
  conn = get_db_connection()
  cursor = conn.cursor()
  
  cursor.execute("""INSERT INTO players (name) VALUES (%s);""", (request.form.get('name'),))
  
  cursor.close()
  conn.commit()
  conn.close()  
  return redirect('/admin')
