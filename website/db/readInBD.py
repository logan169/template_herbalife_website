# -*- coding: utf-8 -*-
from writeInBD import mdp_hash
import sqlite3
from flask_login import UserMixin

conn=sqlite3.connect('db/WellnessGarden', check_same_thread=False)
conn.text_factory = str
c=conn.cursor()


class User(UserMixin):
    def __init__(self, id,username, mail, compte_valide, active):
        self.id = id
        self.username=username
        self.mail = mail
        if compte_valide == 0:
            self.compte_valide = False
        else:
            self.compte_valide = True
        if active == 0:
            self.active = False
        else:
            self.active = True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_compte_valide(self):
        print self.compte_valide
        return self.compte_valide

    def get_id(self):
        return unicode(id)

    def __repr__(self):
        return '<User %r>' % (self.username)



def readProduitDb(titre):
    list=[]
    reqt={"Nutrition_Ciblee":'WHERE gamme="Nutrition Ciblée"',"all":'','remise_en_forme':'WHERE gamme="Remise en Forme"','controle_de_poids':'WHERE gamme="Contrôle de Poids"','sport_&_vitalite':'WHERE gamme="Sport et Vitalité "','soin_du_corps':'WHERE gamme="Soin du Corps"'}

    #affiche la gamme
    if titre in reqt:
        for liste in c.execute('SELECT titre,nom_photo,intro,prix,gamme FROM produits '+reqt[titre]):
            dict={}
            dict['titre']= unicode(liste[0],'utf-8')
            dict['photo']=unicode(liste[1],'utf-8')
            dict['intro']=unicode(liste[2],'utf-8')
            dict['prix']=liste[3]
            dict['gamme']=liste[4]
            list.append(dict)


    #affiche l'item
    else:

        titre=titre.replace('_',' ')

        for liste in c.execute('SELECT titre,nom_photo,intro,description,prix FROM produits WHERE titre=:titre LIMIT 1', [titre]):

            dict={}
            dict['titre']= unicode(liste[0],'utf-8')
            dict['photo']=unicode(liste[1],'utf-8')
            dict['intro']=unicode(liste[2],'utf-8')
            dict['description']=unicode(liste[3],'utf-8')
            dict['prix']=liste[4]
            list.append(dict)

    return list

def ValidateAuth(username,mdp):
    username=str(username)
    mdp=str(mdp)

    dict={}
    for user in c.execute('SELECT salt,mdp FROM user WHERE username=:username ', [username]):
        dict['salt']=user[0]
        dict['mdp']=user[1]
        try:
            if mdp_hash(mdp,dict['salt']) == dict['mdp']:
                return True
            else:
                return False
        except:
            return False

    return False


def verificationUsernameANDMailLibre(username,mail):
    #je ne sais pourquoi mais impossible de verifier autrement que item est non vide sans utiliser cette façon
    for item in c.execute('SELECT username FROM user WHERE username=:username ', [username]):
        return (False,'username')
    for item in c.execute('SELECT mail FROM user WHERE mail=:mail ', [mail]):
        return (False,'mail')
    return (True,'')

def recuperationCompteUserDB(username,mail,nom,prenom):
    #je ne sais pourquoi mais impossible de verifier autrement que item est non vide que de cette façon
    for item in c.execute('SELECT username FROM user WHERE username=:username AND mail=:mail AND nom=:nom AND prenom=:prenom ', [username,mail,nom,prenom]):
        return True
    return False

def findUsername(username):
    c.execute("SELECT * FROM user ", ())
    for item in c.fetchall():
        if str(username) in item[1]:
            return User(item[0],item[1],item[4],item[7],item[8])
        else:
            return None


def nombreItemPanier(mail):
    nombreItem=0
    for item in readPanierDb(mail):
        nombreItem+=item['count']
    return nombreItem

def readPanierDb(username):
    list=[]

    for item in c.execute('SELECT titre, COUNT(titre)FROM panier GROUP BY titre HAVING username=:username ',[username]):

        dict={}
        dict['titre']= unicode(item[0],'utf-8')
        dict['count']= item[1]

        if dict in list:
            list[list.index(dict)]['count']+=1
        else:
            list.append(dict)


    for i in range (len(list)):
        for info in c.execute('SELECT nom_photo,intro,prix FROM produits WHERE titre=:titre_produit',[list[i]['titre']]):

            list[i]['photo']=unicode(info[0],'utf-8')
            list[i]['intro']=unicode(info[1],'utf-8')
            list[i]['prix']=info[2]
    return list




