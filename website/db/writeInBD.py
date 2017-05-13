# -*- coding: iso-8859-1 -*-

import sqlite3
import hashlib, uuid
from time import strftime



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
    c.execute("CREATE TABLE IF NOT EXISTS produits  (gamme_titre VARCHAR PRIMARY KEY,gamme VARCHAR NOT NULL,titre VARCHAR NOT NULL ,nom_photo VARCHAR NOT NULL,intro VARCHAR NOT NULL,description VARCHAR NOT NULL,prix real)")

def tableWriteProduit(game_titre,gamme,titre,nom_photo,intro,description,prix):
    c.execute("INSERT INTO produits VALUES(?,?,?,?,?,?,?)",(game_titre,gamme,titre,nom_photo,intro,description,prix))
    conn.commit()

def createTableUser():
    c.execute("CREATE TABLE IF NOT EXISTS user  (username VARCHAR PRIMARY KEY,nom VARCHAR NOT NULL,prenom VARCHAR NOT NULL,mail VARCHAR NOT NULL,mdp VARCHAR NOT NULL,salt VARCHAR NOT NULL,compte_valide VARCHAR NOT NULL,date1  VARCHAR NOT NULL,date2 REAL)")

def tableWriteUser(username,nom,prenom,mail,motDePasse,compte_valide,date1,date2):
    salt=newSalt()
    mdp=mdp_hash(motDePasse,salt)
    c.execute("INSERT INTO user VALUES(?,?,?,?,?,?,?,?,?)",(username,nom,prenom,mail,mdp,salt,compte_valide,date1,date2))
    conn.commit()

def confirmUser(username):
    c.execute("UPDATE user SET compte_valide = 'TRUE' WHERE username=:username ", [username])
    conn.commit()

def modifyMdp(username,newMdp):
    salt=newSalt()
    mdp=mdp_hash(newMdp,salt)
    c.execute("UPDATE user SET mdp =? WHERE username=? ", [mdp,username,])
    c.execute("UPDATE user SET salt=? WHERE username=? ", [salt,username,])
    conn.commit()

def createTablePanier():
    c.execute("CREATE TABLE IF NOT EXISTS panier (idpanier INTEGER PRIMARY KEY AUTOINCREMENT,username VARCHAR NOT NULL,titre VARCHAR NOT NULL,date CHAR)")

def tableWritePanier(username,titre_produit,date):
    c.execute("INSERT INTO panier VALUES(NULL,?,?,?)",(username,titre_produit,date))
    conn.commit()

def tableRemovePanier(username,titre_produit):
    c.execute("DELETE FROM panier WHERE idpanier in (SELECT idpanier FROM panier WHERE username=:username AND titre=:titre_produit ORDER BY idpanier Limit 1)",(username,titre_produit))
    conn.commit()

createTableProduits()
createTableUser()
createTablePanier()


#tableWriteUser('log169','l','po','log@hotmail.com','lopo23')



colonnes_produits="""
gamme VARCHAR NOT NULL,
titre VARCHAR NOT NULL,
nom_photo VARCHAR NOT NULL,
intro VARCHAR NOT NULL,
description VARCHAR NOT NULL,
prix real,
"""



"""
#script qui rempli la bd produit
def createListe(f):

    file=open(f,"r")
    string=''
    for line in file:
        string+= line.replace('\n','')
    lis=string.split('###')
    return lis

liste_gamme=createListe('gamme')
liste_prix=createListe('prix')
liste_titre=createListe('titre')
liste_photo=createListe('photo')
liste_intro=createListe('intro')
liste_desc=createListe('description')

print len(liste_gamme)
print len(liste_titre)
print len(liste_photo)
print len(liste_intro)
print len(liste_desc)
print len(liste_prix)


for x in range (len(liste_titre)):
    print liste_gamme[x]+'_'+liste_titre[x]
    try:
        tableWriteProduit((liste_gamme[x]+'_'+liste_titre[x]),liste_gamme[x],liste_titre[x],liste_photo[x],liste_intro[x],liste_desc[x],liste_prix[x])
    except:
        continue
"""
