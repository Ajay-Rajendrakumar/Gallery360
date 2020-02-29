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







if __name__ == "__main__":
   
    login = post.query.all()
    print('ID', 'Imgname' ,' Author' , 'Url', 'Views' , 'Likes', "Dislikes")
    for i in login:
        print(i.id, i.imgname, i.author, i.url, i.view, i.like, i.dislike)
   
