#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template,url_for,redirect,request,flash
from flask_mail import Mail,Message
from flask_login import (LoginManager, current_user, login_required,login_user, logout_user, UserMixin,confirm_login, fresh_login_required)
from datetime import timedelta

import itsdangerous as D
from db.token import generate_confirmation_token,confirm_token
from db.readInBD import *
from db.writeInBD import *
import time


app= Flask (__name__)
app.config.update(
    SECRET_KEY = 'm51ze181fsfzedplez15ze78',
    SECURITY_PASSWORD_SALT='actga45zdnlqi453o545ziehqdnc464quycbi56qelncqi864lcqus', #enter SALT for user db management
    REMEMBER_COOKIE_DURATION=timedelta(hours=1),
    MAIL_SERVER = 'smtp.googlemail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    #MAIL_DEBUG = True,
    #TESTING = False,
    MAIL_DEFAULT_SENDER='wellness.garden.website@gmail.com',    #enter server's mail DEFAULT_SENDER
    MAIL_USERNAME = 'wellness.garden.website@gmail.com',        #enter server's mail mail username 
    MAIL_PASSWORD = 'qsdfgh13',                                 #enter server's mail mail password
)

mail = Mail(app)

app_url = '0.0.0.0'#change to your app url
app_port = 8687  #change to your app port
website_url = app_url+':'+str(app_port)

your_mail = '' #enter the mail where you wanna receive  messages from contact view

#this is a variable containing events displayed on events page
##Events
events=[{'titre':'Entrainenement fitness','date':'Tous les mardis a 17h', 'ou':"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2783.2425376262086!2d4.8646515155675845!3d45.76632937910563!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47f4ea86b75937fb%3A0x80a491d5affd1d0b!2s40+Rue+de+la+Viabert%2C+69006+Lyon%2C+France!5e0!3m2!1sfr!2sca!4v1451710630260"}]


@app.route("/")
def init():
    return redirect(url_for('home'))

@app.route('/index')
def home():
    return render_template('accueil.html')


@app.route('/product')
def shop():
    return redirect(url_for('shopGamme', items='all'))

@app.route('/product/<items>',methods=['GET'])
def shopGamme(items):
    items=items.encode('utf-8')
    produitsGamme=readProduitDb(items)
    return render_template('item.html',produits=produitsGamme,identiteVerifiee=True)

@app.route('/evenements')
def evenements():
    return render_template('evenements.html',evenements=events)

@app.route('/contact', methods=['POST','GET'])
def contact():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['mail']
        mess = request.form['message']

        try:
            msg = Message('Wellness Garden',recipients=[your_mail],body='Nom: ' + nom +'\n\nMail: '+email+'\n\nMessage:\n\n'+mess)
            mail.send(msg)
            output_message=unicode('Votre message a bien été envoyé, nous vous répondrons dans les meilleurs délais','utf-8')
        except:
            output_message=unicode('Erreur, le message n\'a pas été envoyé','utf-8')


        flash(output_message)
        return render_template('message.html')

    else:
        return render_template('contact.html')


if __name__ == '__main__':
    app.debug=True
    app.run(host=app_url,port=app_port)
    

