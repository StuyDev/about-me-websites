#! /usr/bin/python


# Flask:           run flask app
# render_template: render webpage
# request:         process data from form
from flask import Flask, render_template, request

import sqlite3




app = Flask(__name__)




# redirect to home page
@app.route('/')
def default():
    return render_template('/index.html');


# home page
@app.route('/index.html')
def index():
    return render_template('/index.html');


# log in page
@app.route('/login.html')
def login():
    return render_template('/login.html');

    

# register page
@app.route('/register.html')
def register():  
    return render_template('/register.html');




# page solely for authorizing log in/registration
@app.route('/auth.html', methods = ['GET', 'POST'])
def auth():


    # KEEP IN THIS METHOD TO AVOID sqlite3.ProgrammingErrot:
    # SQLite objects created in a thread can only be used in that same thread.
    
    # open the database
    connection = sqlite3.connect("database.db")
    database = connection.cursor()
    
    # create the database -- if doesn't already exist
    try:
        database.execute('CREATE TABLE credentials (id REAL, firstName TEXT, lastName TEXT, school TEXT, email TEXT, password TEXT)')
    except sqlite3.OperationalError:
        pass


    
    # if from LOGIN
    if request.method == 'GET':
        uEmail = request.args['email']
        uPass = request.args['pass']
        
        gEmail = database.execute("SELECT email from credentials where email = (?)", [uEmail])
        emailExists = gEmail.fetchone()

        if emailExists:
            # does password match that of email?
            gPass = database.execute("SELECT password from credentials where email = (?)", [uEmail])
            actualPass = gPass.fetchone()

            if uPass == actualPass[0]:
                # fName = database.execute("SELECT firstName from credentials where email = (?)", [uEmail])
                # lName = database.execute("SELECT lastName from credentials where email = (?)", [uEmail])

                connection.commit()
                connection.close()
    
                retStr = "<h1> Hi, " + uEmail + "! </h1> <br>"
                return retStr + render_template('/index.html')

            else:
                connection.commit()
                connection.close()
                
                retStr = "<h1> Incorrect password! </h1> <br>"
                return retStr + render_template('/index.html')
        else:
            connection.commit()
            connection.close()
            
            retStr = "<h1> That e-mail doesn't exist! </h1> <br>"
            return retStr + render_template('/index.html')


        
    # if from REGISTER
    elif request.method == 'POST':
        uFirstName = request.form['firstName']
        uLastName = request.form['lastName']
        uSchool = request.form['school']
        uEmail = request.form['email']
        uPass = request.form['pass']

        # add data
        database.execute('INSERT INTO credentials (firstName, lastName, school, email, password) VALUES ("' + uFirstName + '", "' + uLastName + '", "' + uSchool + '", "' + uEmail + '", "' + uPass + '")')
        
        connection.commit()
        connection.close()
    
        retStr = "<h1> Account created! </h1> <br>"
        return retStr + render_template('/index.html')


    # not GET or POST methods
    else:
        connection.commit()
        connection.close()
    
        retStr = "<h2> There was an HTTP method unaccounted for... </h2> <br>"
        return retStr + render_template('/auth.html')


    connection.commit()
    connection.close()
    

# run the app!
if __name__ == '__main__':
   app.run(debug = True)
