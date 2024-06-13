from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bu3u2yg7812rbas'

boggle_game = Boggle()

@app.route('/')
def homepage() : 
    ''' Shows game board'''
    
    board            = boggle_game.make_board()
    session['board'] = board
    highscore        = session.get('highscore', 0)
    num_plays        = session.get('num_plays', 0)
    
    return render_template('index.html', board=board, highscore = highscore, num_plays = num_plays)


@app.route('/word-check')
def word_check() : 
    '''Check if word is in the dictionary or not'''
    
    word  = request.args['word']
    board = session['board']
    response  = boggle_game.check_valid_word(board, word)
    
    return jsonify({'result': response})

@app.route('/score', methods=['POST'])
def post_score() : 
    '''Obtain score, update the number of plays, and update high score if necessary'''
    
    score     = request.json['score']
    highscore = session.get('highscore', 0)
    num_plays = session.get('num_plays', 0)
    
    session['num_plays'] = num_plays + 1
    session['highscore'] = max(score, highscore)
    
    return jsonify(brokeRecord = score > highscore)