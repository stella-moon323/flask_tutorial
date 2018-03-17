from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hello.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

    def __init__(self, username):
        self.username = username


@app.route('/')
def hello():
    user_list = User.query.all()
    return render_template('hello.html', user_list=user_list)


@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form.get('username')
    if username:
        user = User(username)
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('hello'))
    

@app.route('/user/<int:user_id>', methods=['GET'])
def show_user(user_id):
    target_user = User.query.get(user_id)
    return render_template('show.html', target_user=target_user)


@app.route('/user/<int:user_id>', methods=['POST'])
def mod_user(user_id):
    target_user = User.query.get(user_id)
    username = request.form.get('username')
    if target_user and username:
        target_user.username = username
        db.session.commit()
    return redirect(url_for('hello'))


@app.route('/del_user/<int:user_id>', methods=['POST'])
def del_user(user_id):
    target_user = User.query.get(user_id)
    if target_user:
        db.session.delete(target_user)
        db.session.commit()
    return redirect(url_for('hello'))


if __name__ == '__main__':
    app.run(debug=True)

