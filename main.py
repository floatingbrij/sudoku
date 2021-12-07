
from flask import Flask, render_template, redirect, request, session, jsonify
from flask_session import Session
import suduko as s

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.get('/')
def sudoku():

    if not session.get("sudokulist"):
        a = s.createboard(3)
        session["sudokulist"] = a
        session["diff"] = 3
    else:
        a = session["sudokulist"]
    return render_template('basefiles/base1.html', sudoku = a)

@app.post('/')
def sudokupost():
    data = request.json
    if data["type"] == "check":
        a = s.checkboard(data["board"])
        print(data,a)
        return jsonify(a)
    if data["type"] == "reset":
        return jsonify(session["sudokulist"])
    if data["type"] == "solve":
        usersolve = s.solve(data["board"])
        print("user: ",usersolve)
        if usersolve == False:
            print("session:",s.solve(session["sudokulist"]))
            return jsonify(s.solve(session["sudokulist"]))      
        return jsonify(usersolve)
    if data["type"] == "newgame":
        a = s.createboard(session["diff"])
        session["sudokulist"] = a
        
        return jsonify(a)
    if data["type"] == "setdiff":
        session["diff"]= data["diff"]
        
        return jsonify(True)



  
if __name__ == '__main__':
    
    app.run(host='0.0.0.0')
    
    
    