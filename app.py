from flask import Flask, Blueprint, current_app, g, render_template, redirect, request, flash, url_for
from flask.cli import with_appcontext

import sqlite3
import click

import random
import string
app = Flask(__name__)

# database management
message_db = Blueprint('message', __name__, url_prefix='/message')

def main():
    return render_template("main_better.html")

def get_message_db():
    # creates the database of messages
    if 'db' not in g:
        g.message_db = sqlite3.connect("messages_db.sqlite")

    return g.message_db

def close_message_db(e=None):
    db = g.pop('auth_db', None)

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
    click.echo('Initialized the user database.')

def insert_message(request):
    #  inserts a user message into the database of messages
    message = request.form['message']
    handle = request.form['handle']
    db = get_message_db()
    error = None
    m = db.execute(
        'SELECT * FROM m WHERE message = ?', (message,)
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
            'INSERT INTO m (message, handle) VALUES (?, ?)',
            (message, handle)
        )
        db.commit()
        flash('Message succesfully saved!.')
        return redirect(url_for('submit.html'))
    flash(error)

# posting basic user data
@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')

    else:
        insert_messages(n)

    return render_template('auth/register.html')


app.register_blueprint(message_db)
app.teardown_appcontext(close_message_db)
app.cli.add_command(init_message_db_command)