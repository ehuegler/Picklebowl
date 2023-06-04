from flask import Flask, render_template, json, redirect, request
from dataclasses import dataclass

@dataclass
class Player:
  name: str
  
  def getWins(this):
    return 0
  
  def getLoses(this):
    return 0
  
  def getSetDiff(this):
    return 0
  
@dataclass
class Game:
  homePlayer: Player
  awayPlayer: Player
  homeScore: int
  awayScore:int

app = Flask(__name__)

games = []
players = []

# ethan = Player('Ethan')
# brian = Player('Brian')
# players = [ethan, brian]

@app.route('/')
def home():
    return render_template('index.html', players=players, games=games)
  
@app.route('/admin')
def admin():
  return render_template('admin.html')

@app.route('/save')
def save():
  return json.dumps([players, games])

@app.route('/upload', methods=['POST'])
def upload():
  global players
  global games
  players = []
  games = []
  
  data = json.loads(request.form.get('seasonData'))
  
  for player in data[0]:
    players.append(Player(player['name']))
    
  for game in data[1]:
    games.append(Game(game['homePlayer'], game['awayPlayer'], game['homeScore'], game['awayScore']))
  
  return redirect('/admin')

@app.route('/newGame', methods=['POST'])
def newGame():
  global games
  global players
  
  # check the players exist here
  
  games.append(Game(request.form.get('homePlayer'), request.form.get('awayPlayer'), request.form.get('homeScore'), request.form.get('awayScore')))  
  
  return redirect('/admin')

@app.route('/newPlayer', methods=['POST'])
def newPlayer():
  global players
  
  players.append(Player(request.form.get('name')))
  
  return redirect('/admin')
