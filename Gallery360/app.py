from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
import os
import requests
from PIL import Image
from os.path import basename

user_id=0

file=os.path.abspath(os.getcwd())+'/database.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file
db = SQLAlchemy(app)


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

class post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80))
    imgname = db.Column(db.String(80))
    url = db.Column(db.String(100))
    view = db.Column(db.Integer)
    like = db.Column(db.Integer)
    dislike = db.Column(db.Integer)


class feel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id=db.Column(db.String(80))
    image_id=db.Column(db.String(80))
    status=db.Column(db.Integer)

class view(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id=db.Column(db.String(80))
    image_id=db.Column(db.String(80))
    status=db.Column(db.Integer)




@app.route("/")
def index():
    return render_template("index.html")



@app.route("/login",methods=["GET", "POST"])
def login():

    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        
        login = user.query.filter_by(username=uname, password=passw).first()

        
        if login is not None:
            pid = user.query.filter_by(username=uname).first()
            print(pid)
            global user_id
            user_id=pid
            return redirect(url_for("Main",name=uname))

    return render_template("login.html") 
    
    

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        register = user(username = uname, email = mail, password = passw)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        uname = request.form['uname']
        url = request.form['url']

  
    image = Image.open(url)
    if(image):
        file=os.path.abspath(os.getcwd())
        base=basename(url)
        loc=file+'/static/thumb/'+base
        image.save(loc,quality=20,optimize=True)
        register = post(author = uname,imgname=base,url=url, view = 0, like = 0,dislike = 0)
        db.session.add(register)
        db.session.commit()           
    return redirect(url_for("Main",name=uname))

@app.route("/Main", methods=["GET", "POST"])
def Main():
    #db.session.query(post).delete()
    #db.session.commit()
    posts=post.query.all()
    views=[]
    like=[]
    Allpost=[]
    for i in posts:
        temp=[]
        temp.append(i.id)
        val=view.query.filter_by(image_id=i.id).first()
        if(val):
            views.append(val)
        else:
            views.append(0)
        val=feel.query.filter_by(image_id=i.id).first()
        if(val):
            like.append(val)
        else:
            like.append(0)
        temp.append(i.author)
        temp.append(i.imgname)
        temp.append(i.url)        
        temp.append(i.view)
        temp.append(i.like)
        temp.append(i.dislike)
        Allpost.append(temp)
        del temp
    return render_template('Main.html',name=request.args.get('name'),posts=Allpost)


@app.route("/like", methods=["GET", "POST"])
def like():
    if request.method == "POST":
        post_id = request.form['data']
    obj = post.query.filter_by(id=post_id).first()
    state = feel.query.filter_by(author_id=user_id,image_id=post_id).first()
    if state is not None:
        obj.like +=1
        register = feel(author_id=user_id,image_id=post_id,status=1)
        db.session.add(register)
        db.session.commit()   
    
    return render_template('Main.html')    



@app.route("/unlike", methods=["GET", "POST"])
def unlike():
    if request.method == "POST":
        post_id = request.form['data']
    
    obj = post.query.filter_by(id=post_id).first()
    state = feel.query.filter_by(author_id=user_id,image_id=post_id).first()
    if state is not None:
        obj.dislike +=1
        register = feel(author_id=user_id,image_id=post_id,status=-1)
        db.session.add(register)
        db.session.commit()

    return render_template('Main.html')    


 

@app.route("/show360/<int:pid>", methods=["GET", "POST"])
def show360(pid):
    obj = post.query.filter_by(id=pid).first()
    state = view.query.filter_by(author_id=user_id,image_id=pid).first()
    if state is None:
        obj.view +=1
        register = view(author_id=user_id,image_id=pid,status=1)
        db.session.add(register)
        db.session.commit()
    url='/static/'+obj.imgname
    return render_template("360.html", img = url)  


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)