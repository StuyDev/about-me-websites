from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


admin = User(username='admin', email='admin@example.com')
guest = User(username='guest', email='guest@example.com')

db.create_all()

db.session.add(admin)
db.session.add(guest)
db.session.commit()

User.query.all()



@app.route('/')

def doThis():
    retStr = "<h1> Raymond Wu </h1>"
    retStr += "Things I like"
    retStr += '<ol start="0">'
    retStr += "<li> Lists that start with 0 </li>"
    retStr += "<li> Computer science </li>"
    retStr += "<li> Programming </li>"
    retStr += "</ol>"
    retStr += "<br>"
    retStr += "Some more text here"
    retStr += "<br><br>"
    retStr += '<a href="/pageTwo"> Go to page 2</a>'
    return retStr

@app.route("/pageTwo")
def doThat():
    retStr = "<h2> Welcome to page 2! </h2>"
    retStr += "Some more text here"
    retStr += "<br><br>"
    retStr += '<a href="/"> Go back to page 1 </a>'
    return retStr

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/login")
def login():
    return render_template('login.html')




if __name__ == '__main__':
    app.run(debug=True)

