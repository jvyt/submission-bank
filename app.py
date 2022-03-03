from flask import Flask, Blueprint, current_app, g, render_template, redirect, request, flash, url_for
from flask.cli import with_appcontext

import sqlite3
import click

import random
import string
app = Flask(__name__)

# database management
message_db = Blueprint('message', __name__, url_prefix='/submit')

def main():
    return render_template("main_better.html")

def get_message_db():
    # creates the database of messages
    if 'db' not in g:
        g.message_db = sqlite3.connect("messages_db.sqlite")

        g.message_db.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER, handle TEXT, message TEXT)")

    return g.message_db

def insert_message(request):
    message = request.form["message"]
    user = request.form["handle"]

    db = get_message_db()

    # count the number of rows
    total_num_rows = db.execute("SELECT COUNT(*) FROM messages")

    id_num = int(total_num_rows.fethcall()[0][0]) + 1

    db.execute("INSERT INTO messages (id, handle, message VALUES (?, ?, ?)", (id_num, user, message))

    db.commit()
    db.close()

def random_messages(n):
    db = get_message_db()
    rand = db.execute("SELECT message, handle FROM messages ORDER BY RANDOM() LIMIT ?", (n,))
    
    collection = rand.fetchall()

    db.close()
    return collection

def close_message_db(e=None):
    db = g.pop('message_db', None)

    if db is not None:
        db.close()

def init_message_db():
    db = get_message_db()

    with current_app.open_resource('init.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init_message_db')
@with_appcontext
def init_message_db_command():
    """Clear the existing data and create new tables."""
    init_message_db()
    click.echo('Initialized the message database.')

def insert_message(request):
    #  inserts a user message into the database of messages
    # handle = request.form['handle']
    db = get_message_db()
    error = None
    m = db.execute(
        'SELECT * FROM messages WHERE request = ?', (request,)
        ).fetchone()

    if not message:
            error = 'A message is required.'
    elif not handle:
        error = 'A handle is required.'
    elif db.execute(
        'SELECT id FROM m WHERE message = ?', (message,)
    ).fetchone() is not None:
        error = f"User with Handle, {handle}, is already registered."

    if error is None:
        db.execute(
            "INSERT INTO m (id, handle, message) VALUES (?,?,?);",(id, message, handle)
        )
        db.commit()
        db.close()

        flash('Message succesfully saved!.')
        return redirect(url_for('submit.html'))
    flash(error)

# posting basic user data
@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')

    else:
        try:
            insert_message(request)
            return render_template('submit.html', thanks = True)
        
        except:
            return render_template('submit.html', error = True)

@app.route('/view/', methods = ['POST', 'GET'])
def view():
    if request.method == 'GET':
        return render_template('view.html')

    else:
        try:
            rand = random_messages(int(request.form['num']))
            message = random_messages(rand)
            return(render_template('view.html', message))
        except: 
            return render_template('view.html', error = True)