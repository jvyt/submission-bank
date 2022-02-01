from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
# simplest possible approach
# def main():
#     return "hi there!"


# slightly less trivial
# def main():
#     return render_template("main.html")

# A little fancier

# @app.route("/")
def main():
    return render_template("main_better.html")

# getting basic user data
@app.route('/submit/', methods=['POST', 'GET'])
def ask():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        try:
            return render_template('submit.html', name=request.form['name'], student=request.form['student'])
        except:
            return render_template('submit.html')

# 
@app.route('/profile/<name>/')
def hello_name(name):
    return render_template('profile.html', name=name)