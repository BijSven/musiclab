from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import g

from youtubesearchpython import VideosSearch, ChannelSearch

import sqlite3
import random

DATABASE = 'static/storage/main.sqlite'

app = Flask(__name__, template_folder='static/web')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.args.get('token') is not None:
        if request.method == 'POST':
            try:
                song_name = request.form['songName']
                instrument = request.form['instrument']
                try:
                    try:
                        resultsData = ChannelSearch(f"{song_name}", "UCts9lFixyOqwhGCEbXErPwA")
                        resultData = resultsData.result()

                        result = resultData['result'][0]['link']
                        result = result.split('=')[1]
                    except:
                        resultsData = ChannelSearch(f"{song_name}", "UCfMZNJ5CDIQ5EusW4SQcMMg")
                        resultData = resultsData.result()

                        result = resultData['result'][0]['link']
                        result = result.split('=')[1]
                except:
                    resultsData = VideosSearch(f"{song_name} - {instrument}")
                    resultData = resultsData.result()

                    result = resultData['result'][0]['link']
                    result = result.split('=')[1]

                db = get_db()
                with db:
                    cr = db.cursor()
                    cr.execute('UPDATE `player` SET `song` = ? WHERE `party` = ?', (result, (request.args.get('token'))))

                newURL = url_for('admin', token=(request.args.get('token')))
                return redirect(newURL)
            except:
                return 'This number does not exist, some error occurred!<br>Please check if your search has been typed correctly!'
        else:
            return render_template('admin/main.html')
    else:
        if request.method == 'POST':
            token = request.form['code']
            if(all(char.isalnum() or char == '-' for char in token)):
                newURL = url_for('admin', token=token)
                return redirect(newURL)
            else:
                return redirect('admin')
        
        return render_template('admin/connect.html')

@app.route('/', methods=['GET', 'PING'])
def index():
    if request.method == 'GET':
        if request.args.get('session') is None:
            code = generate_code()
            db = get_db()
            with db:
                cr = db.cursor()
                cr.execute('INSERT INTO `player` (`party`, `song`) VALUES (?, ?)', (code, 'dQw4w9WgXcQ'))
                newURL = url_for('index', session = code)
                return redirect(newURL)
        else:
            try:
                code = request.args.get('session')
                db = get_db()
                with db:
                    cr = db.cursor()
                    c1 = cr.execute('SELECT `song` FROM `player` WHERE `party` = ?', (code,))
                    r1 = c1.fetchone()[0]
                    if (r1 == 'dQw4w9WgXcQ'):
                        return render_template('client/client.html', TOKEN = code)
                    else:
                        newURL = url_for('index', session = code)
                        return render_template('client/viewer.html', videoURL = r1)
            except Exception as e:
                print(e)
                newURL = url_for('index')
                return redirect(newURL)
    if request.method == 'PING':
        code = request.args.get('session')
        db = get_db()
        try:
            with db:
                cr = db.cursor()
                c1 = cr.execute('SELECT `song` FROM `player` WHERE `party` = ?', (code,))
                r1 = c1.fetchone()[0]
                return r1
        except:
            return 'Yeah, this doesnt work!'

def generate_code():
    code = ""

    for _ in range(1):
        code += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        code += str(random.randint(0, 9))
        code += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        code += str(random.randint(0, 9))
        code += "-"

    code += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    code += str(random.randint(0, 9))
    code += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    code += str(random.randint(0, 9))

    return code

if __name__ == '__main__':
    app.run()