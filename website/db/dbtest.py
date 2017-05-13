# -*- coding: iso-8859-1 -*-

import sqlite3

import hashlib, uuid
import chardet


###############################################################"
##mdp
###############################################################

#create a salt
def newSalt():
    return uuid.uuid4().hex

#hash mdp avec le salt
def mdp_hash(mdp,salt):
    return hashlib.sha512(mdp + salt).hexdigest()

###############################################################

conn=sqlite3.connect('db/WellnessGarden', check_same_thread=False)
conn.text_factory = str
c=conn.cursor()

def delTable(table):
    c.execute('DELETE FROM '+str(table))

def createTableProduits():
    c.execute("CREATE TABLE IF NOT EXISTS produits (id INTEGER PRIMARY KEY AUTOINCREMENT,gamme text,titre text,nom_photo text,intro text,description text,prix real)")

def tableWriteProduit(gamme,titre,nom_photo,intro,description,prix):
    c.execute("INSERT INTO produits VALUES(?,?,?,?,?,?)",(gamme,titre,nom_photo,intro,description,prix))
    conn.commit()

def createTableUser():
    c.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT,nom text,prenom text,mail text,mdp text,salt text)")

def tableWriteUser(nom,prenom,mail,motDePasse):
    salt=newSalt()
    mdp=mdp_hash(motDePasse,salt)
    c.execute("INSERT INTO user VALUES(?,?,?,?,?)",(nom,prenom,mail,mdp,salt))
    conn.commit()

def createTablePanier():
    c.execute("CREATE TABLE IF NOT EXISTS panier (id_panier INTEGER PRIMARY KEY AUTOINCREMENT, id_user VARCHAR, id_produit INTEGER,FOREIGN KEY (id_user) REFERENCES user(id),FOREIGN KEY (id_produit) REFERENCES produit(id))")

def tableWritePanier(id_user,id_produit):
    c.execute("INSERT INTO panier VALUES(?,?)",(id_user,id_produit))
    conn.commit()

def tableRemovePanier(id_user,id_produit):
    c.execute("DELETE FROM panier WHERE id_produit = (SELECT id FROM produit WHERE mail=:mail AND titre=:titre_produit ORDER BY titre LIMIT 1)",(mail,titre_produit))
    conn.commit()

createTablePanier()
createTableUser()
createTableProduits()
'''
tableWriteProduit(u'Soin du Corps',u'Soin du Corps',u'Soin du Corps',u'Soin du Corps',u'Soin du Corps',20)
tableWriteUser('log','p','log@o.com','lolo')
tableWritePanier()
'''

colonnes_produits='''
gamme text,
titre text,
nom_photo text,
intro text,
description text,
prix real,
'''




file=open('.\db\liste.txt',"r")
for line in file:
    #l=(line.split(','))
    print line.split(',')
    #tableWriteProduit(l[0],l[1],l[2],l[3],l[4],l[5])