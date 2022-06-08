from os import truncate
import sqlite3
from tkinter import *

fenTuto = Tk()
fenTuto.config(width=450,height=400,bg='#B0F4FD')
fenTuto.title("Tutoriel")
#Fenêtre en mode pop-up
intro = Label(fenTuto,text="Voici le logiciel de création d'arbre généalogique."+'\n'+
"Voici comment l'utiliser :"+'\n'+
"Rentrez le nom et le prénom de la personne désirée. "+'\n'+
"Ensuite vous pouvez le rechercher via le bouton "+'\n'+
"Recherche qui vous permettra aussi de modifier "+'\n'+
"ses informations (en maintenance). "+'\n'+
"Vous pouvez aussi cliquez sur créer un arbre pour "+'\n'+
"créer un arbre généalogique sur 3 générations "+'\n'+
"ascendantes avec la personne sélectionnée comme "+'\n'+
"racine."+'\n'+
"En cliquant sur une case comportant un nom, "+'\n'+
"les informations de la personne s'afficheront. "+'\n'+
"En cliquant sur une case sans information, une "+'\n'+
"fenêtre de création de personne s'ouvrira")
intro.place(x=0,y=5)
intro.config(font=('verdana',12,'normal'), justify='left',bg='#B0F4FD')

fenTuto.mainloop()

fenetre = Tk() #Création de la fenêtre principale
fenetre.config(width=800,height=650,bg='#B0F4FD') #Configuration de cette fenêtre
fenetre.title("Arbre généalogique") #Titre de la fenêtre
#Initialisation de variables
Nom = None
Prenom = None
mariageInfo = None
objet=True
drapeau=False

def EstDedans():
    '''Cette fonction permet de savoir si la personne sélectionnée est dans la base de données. Elle returne True ou False'''
    connexion = sqlite3.connect("base.db") #Connexion avec la base de données
    curseur = connexion.cursor() #Création d'un curseur
    global drapeau,Nom,Prenom,tempNom,tempPrenom #Mise en global des variables
    if Nom==None and Prenom==None or Nom!=entreeNom.get() and Prenom != entreePrenom.get() :
        Nom = entreeNom.get()
        Prenom = entreePrenom.get()
    curseur.execute("SELECT Nom, Prenom FROM Personne")
    total = curseur.fetchall()
    for instance in total:
        tempNom=instance[0]
        tempPrenom=instance[1]
        if tempNom == Nom and tempPrenom == Prenom:
            drapeau = True
    connexion.commit() #Sauvegarde du fichier
    connexion.close() #Déconnexion avec le fichier
    return drapeau


def DateNaissance(donnee):
    '''Cette fonction renvoie les informations de la naissance liées à la personne demandée'''
    connexion = sqlite3.connect("base.db")
    curseur = connexion.cursor()
    curseur.execute("SELECT Naissance.Date,Lieu.Ville,Lieu.Adresse FROM Naissance JOIN Personne \
                    ON Naissance.Id_Naissance=Personne.Id_Naissance JOIN Lieu ON Naissance.Id_Lieu=Lieu.Id_Lieu \
                    WHERE Personne.Nom=? AND Personne.Prenom=?",donnee)
    dateNaissance = curseur.fetchall()
    if dateNaissance == []:
        return("Pas d'info")
    else:
        for instance in dateNaissance:
            tempNaissance=instance[0]
            tempNaissanceLieu=instance[1]
            tempNaissanceAdresse=instance[2]
            return((tempNaissance,tempNaissanceLieu,tempNaissanceAdresse))
    connexion.commit()
    connexion.close()

def Deces(donnee):
    '''Cette fonction renvoie les informations du décès liées à la personne demandée'''
    connexion = sqlite3.connect("base.db")
    curseur = connexion.cursor()
    curseur.execute("SELECT Deces.Date,Lieu.Ville FROM Deces JOIN Personne ON Personne.Id_Deces=Deces.Id_Deces \
                    JOIN Lieu ON Deces.Id_Lieu=Lieu.Id_Lieu WHERE Personne.Nom=? AND Personne.Prenom=?",donnee)
    deces=curseur.fetchall()
    if deces == []:
        return("Pas d'info ou non mort")
    else:
        for instance in deces:
            tempDeces=instance[0]
            tempDecesLieu=instance[1]
            return(tempDeces,tempDecesLieu)
    connexion.commit()
    connexion.close()

def Mariage(donnee):
    '''Cette fonction renvoie les informations de mariage liées à la personne demandée'''
    global mariageInfo
    connexion = sqlite3.connect("base.db")
    curseur = connexion.cursor()
    donnee=(donnee+donnee)
    curseur.execute("SELECT Mariage.Date,Lieu.Ville,Epoux.Nom,Epoux.Prenom,Epouse.Nom,Epouse.Prenom \
                    From Mariage JOIN Lieu ON Lieu.Id_Lieu=Mariage.Id_Lieu JOIN Personne AS Epoux ON Mariage.Id_Epoux=Epoux.Id_personne \
                    JOIN Personne AS Epouse ON Mariage.Id_Epouse=Epouse.Id_personne WHERE (Epoux.Nom=? AND Epoux.Prenom=?) \
                    OR (Epouse.Nom=? AND Epouse.Prenom=?)",donnee)
    mariage=curseur.fetchall()
    mariageInfo=None
    if mariage == []:
        connexion.commit()
        connexion.close()
        return("Pas d'info ou non marié")
    else:
        for instance in mariage:
            tempMariage=instance[0]
            tempMariageLieu=instance[1]
            tempMariageEpouxNom=instance[2]
            tempMariageEpouxPrenom=instance[3]
            tempMariageEpouseNom=instance[4]
            tempMariageEpousePrenom=instance[5]
        mariageInfo=(tempMariageEpouxNom,tempMariageEpouxPrenom,tempMariageEpouseNom,tempMariageEpousePrenom)
        connexion.commit()
        connexion.close()
        return(tempMariage,tempMariageLieu,tempMariageEpouxNom,tempMariageEpouxPrenom,tempMariageEpouseNom,tempMariageEpousePrenom)


def Enfant(donnee):
    '''Cette fonction renvoie les informations des enfants liées à la personne demandée'''
    global mariageInfo
    connexion = sqlite3.connect("base.db")
    curseur = connexion.cursor()
    donnee=(donnee+donnee)
    curseur.execute("SELECT Enfant.Nom, Enfant.Prenom FROM Personne AS Enfant Join Personne AS Pere \
                    ON Enfant.Id_Pere=Pere.Id_personne JOIN Personne AS Mere ON Enfant.Id_Mere=Mere.Id_personne \
                    WHERE Pere.Nom=? AND Pere.Prenom=? AND Mere.Nom=? AND Mere.Prenom=?",donnee)
    enfant=curseur.fetchall()
    nomEnfantStr=None
    prenomEnfantStr=None
    enfantStr=[]
    for i in range(len(enfant)-1):
        nomEnfantStr=enfant[i][i]
        prenomEnfantStr=enfant[i][i+1]
        enfantStr=enfantStr+[nomEnfantStr,prenomEnfantStr]
    connexion.commit()
    connexion.close()
    return(enfant)

def Ajouter(varParent):
    '''Cette fonction est déclenchée lorsque l'on appuie sur une personne sans information'''
    print(Nom,Prenom)
    def Ajout():
        '''Cette fonction est déclenchée lors de l'appuie du bouton enregistrer de la fenêtre d'ajout d'une personne'''
        print("Ajout")
        nomInfo=entreeNomInfo.get() 
        prenomInfo=entreePrenomInfo.get()
        identiteInfo=(nomInfo,prenomInfo)
        connexion = sqlite3.connect("base.db")
        curseur = connexion.cursor()
        curseur.execute("INSERT INTO Personne(Nom,Prenom) VALUES (?,?);",identiteInfo)
        connexion.commit()
        connexion.close()

        naissanceDateInfo=entreeNaissanceDate.get() #Date de Naissance
        naissanceLieuInfo=entreeNaissanceLieu.get()
        naissanceAdresseInfo=entreeNaissanceAdresse.get()
        naissanceInfo1=(naissanceDateInfo,naissanceLieuInfo,naissanceAdresseInfo)
        naissanceInfo2=(naissanceLieuInfo,naissanceAdresseInfo)
        connexion = sqlite3.connect("base.db")
        curseur = connexion.cursor()
        curseur.execute("INSERT INTO Lieu(Ville,Adresse) VALUES (?,?);",naissanceInfo2)
        curseur.execute("INSERT INTO Naissance(Date,Id_Lieu) VALUES (?,(SELECT Lieu.Id_Lieu FROM Naissance \
                        JOIN Lieu ON Naissance.Id_Lieu=Lieu.Id_Lieu WHERE Lieu.Ville=? AND Lieu.Adresse=?));",naissanceInfo1)
        connexion.commit()
        connexion.close()

        mariageDateInfo=entreeMariageDate.get() #Mariage
        mariageLieuInfo=entreeMariageLieu.get()
        mariageEpouxNomInfo=entreeMariageEpouxNom.get()
        mariageEpouxPrenomInfo=entreeMariageEpouxPrenom.get()
        mariageEpouseNomInfo=entreeMariageEpouseNom.get()
        mariageEpousePrenomInfo=entreeMariageEpousePrenom.get()
        mariageInfo1=(mariageLieuInfo)
        mariageInfo2=(mariageDateInfo,mariageLieuInfo,mariageEpouxNomInfo,mariageEpousePrenomInfo)
        connexion = sqlite3.connect("base.db")
        curseur = connexion.cursor()
        curseur.execute("INSERT INTO Lieu(Ville) VALUES (?);",mariageInfo1)
        curseur.execute("INSERT INTO Mariage(Date,Id_Lieu,Id_Epoux) VALUES (?,(SELECT Naissance.Id_Naissance \
                        FROM Naissance JOIN Lieu ON Naissance.Id_Lieu=Lieu.Id_Lieu WHERE Lieu.Ville=?),(SELECT Epoux.Id_personne \
    	                FROM Personne AS Epoux WHERE Epoux.Nom=? AND Epoux.Prenom=?));",mariageInfo2)
        connexion.commit()
        connexion.close()

        personneInfo=(naissanceDateInfo,nomInfo,prenomInfo) #Id_Naissance dans 
        connexion = sqlite3.connect("base.db")
        curseur = connexion.cursor()
        curseur.execute("UPDATE Personne SET Id_Naissance=(SELECT Id_Naissance FROM Naissance WHERE Date=?) \
                        WHERE Nom=? AND Prenom=?",personneInfo)
        connexion.commit()
        connexion.close()

        if varParent=="père":
            donnee=(nomInfo,prenomInfo,Nom,Prenom) #Id_Mère
            connexion = sqlite3.connect("base.db")
            curseur = connexion.cursor()
            curseur.execute("UPDATE Personne SET Id_Pere=(SELECT Id_personne FROM Personne WHERE Nom=? AND Prenom=?) \
            WHERE Nom=? AND Prenom=?",donnee)
        if varParent=="mère":
            donnee=(nomInfo,prenomInfo,Nom,Prenom) #Id_Mère
            connexion = sqlite3.connect("base.db")
            curseur = connexion.cursor()
            curseur.execute("UPDATE Personne SET Id_Mere=(SELECT Id_personne FROM Personne WHERE Nom=? AND Prenom=?) \
            WHERE Nom=? AND Prenom=?",donnee)


    #Création de la fenêtre
    fenAjouter = Toplevel()
    fenAjouter.config(width=500,height=450,bg='#B0F4FD')
    fenAjouter.title("Ajouter une personne")
    #Fenêtre en mode pop-up
    fenAjouter.grab_set()
    fenAjouter.transient(fenAjouter.master)

    texteNomInfo=Label(fenAjouter,text="Nom :") #Nom
    texteNomInfo.place(x=5,y=10) 
    entreeNomInfo=Entry(fenAjouter)
    entreeNomInfo.place(x=100,y=9)
    textePrenomInfo=Label(fenAjouter,text="Prénom :") #Prénom
    textePrenomInfo.place(x=5,y=40)
    entreePrenomInfo=Entry(fenAjouter)
    entreePrenomInfo.place(x=100,y=39)


    texteNaissanceDate=Label(fenAjouter,text="Est né le :") #Date de Naissance
    texteNaissanceDate.place(x=5,y=70)
    entreeNaissanceDate=Entry(fenAjouter)
    entreeNaissanceDate.place(x=100,y=69)
    texteNaissanceLieu=Label(fenAjouter,text="à :") #Lieu de Naissance
    texteNaissanceLieu.place(x=5,y=100)
    entreeNaissanceLieu=Entry(fenAjouter)
    entreeNaissanceLieu.place(x=100,y=99)
    texteNaissanceAdresse=Label(fenAjouter,text="au :") #Adresse de Naissance
    texteNaissanceAdresse.place(x=230,y=100)
    entreeNaissanceAdresse=Entry(fenAjouter)
    entreeNaissanceAdresse.place(x=290,y=99)


    texteMariageDate=Label(fenAjouter,text="Marié le :") #Date de mariage
    texteMariageDate.place(x=5,y=130)
    entreeMariageDate=Entry(fenAjouter)
    entreeMariageDate.place(x=100,y=129)
    texteMariageLieu=Label(fenAjouter,text="à :") #Lieu du mariage
    texteMariageLieu.place(x=230,y=130)
    entreeMariageLieu=Entry(fenAjouter)
    entreeMariageLieu.place(x=290,y=129)
    texteMariageEpouxNom=Label(fenAjouter,text="Les mariés sont :") #Nom du marié 1
    texteMariageEpouxNom.place(x=5,y=160)
    entreeMariageEpouxNom=Entry(fenAjouter)
    entreeMariageEpouxNom.place(x=100,y=159)
    entreeMariageEpouxPrenom=Entry(fenAjouter) #Prénom du marié 1
    entreeMariageEpouxPrenom.place(x=200,y=159)
    texteMariageEpouseNom=Label(fenAjouter,text="Marié le :") #Nom du marié 2
    texteMariageEpouseNom.place(x=5,y=190)
    entreeMariageEpouseNom=Entry(fenAjouter)
    entreeMariageEpouseNom.place(x=100,y=189)
    entreeMariageEpousePrenom=Entry(fenAjouter) #Prénom du marié 2
    entreeMariageEpousePrenom.place(x=200,y=189)
    texteEnfantNom=Label(fenAjouter,text="Son enfant est :") #Enfant issu mariage
    texteEnfantNom.place(x=5,y=220+30)
    entreeEnfantNom=Entry(fenAjouter)
    entreeEnfantNom.place(x=100,y=219+30)
    entreeEnfantPrenom=Entry(fenAjouter) #Prénom enfant
    entreeEnfantPrenom.place(x=200,y=219+30)

    boutonValider=Button(fenAjouter,text="Valider les modifications",command=Ajout) #Bouton de validation
    boutonValider.config(bg='orange')
    boutonValider.place(x=150,y=350)


def Recherche():
    '''Cette fonction se déclenche suite à l'action du bouton Recherche. Il permet d'ouvrir une interface de recherche et 
    de modifications de la personne donnée si elle est présente dans la base de données'''
    global donnee,Nom,Prenom
    if EstDedans():
        fenInfo = Toplevel()
        fenInfo.config(width=500,height=450,bg='#B0F4FD')
        fenInfo.title("Configuration et informations")
        #Fenêtre en mode pop-up
        fenInfo.grab_set()
        fenInfo.transient(fenInfo.master)

        def Modification():
            '''Cette fonction permet de modifier les données d'une personne suite à la validation de ces dernières par le bouton 
            Valider'''
            nomInfo=entreeNomInfo.get() #Nom et Prénom
            prenomInfo=entreePrenomInfo.get()
            donneeInfo=(nomInfo,prenomInfo,donnee)
            connexion = sqlite3.connect("base.db")
            curseur = connexion.cursor()
            curseur.execute("UPDATE Personne SET Nom=?,Prenom=? WHERE Nom=? AND Prenom=?",donneeInfo)
            connexion.commit()
            connexion.close()

            naissanceDateInfo=entreeNaissanceDate.get() #Date de Naissance
            naissanceLieuInfo=entreeNaissanceLieu.get()
            naissanceAdresseInfo=entreeNaissanceAdresse.get()
            naissanceInfo1=(naissanceDateInfo,Nom,Prenom)
            naissanceInfo2=(naissanceLieuInfo,naissanceAdresseInfo,Nom,Prenom)
            connexion = sqlite3.connect("base.db")
            curseur = connexion.cursor()
            curseur.execute("UPDATE Naissance SET Date =? WHERE Naissance.Id_Naissance=(SELECT Personne.Id_Naissance \
							FROM Personne JOIN Naissance ON Personne.Id_Naissance=Naissance.Id_Naissance \
							WHERE Personne.Nom=? AND Personne.Prenom=?)",naissanceInfo1)
            curseur.execute("UPDATE Lieu SET Ville=?, Adresse=? WHERE Lieu.Id_Lieu=(SELECT Naissance.Id_Lieu \
							FROM Naissance JOIN Lieu ON Lieu.Id_Lieu=Naissance.Id_Lieu \
                            WHERE Naissance.Id_Naissance=(SELECT Personne.Id_Naissance FROM Personne JOIN Naissance \
							ON Personne.Id_Naissance=Naissance.Id_Naissance \
							WHERE Personne.Nom=? AND Personne.Prenom=?))",naissanceInfo2)
            connexion.commit()
            connexion.close()

            mariageDateInfo=entreeMariageDate.get() #Mariage
            mariageLieuInfo=entreeMariageLieu.get()
            mariageEpouxNomInfo=entreeMariageEpouxNom.get()
            mariageEpouxPrenomInfo=entreeMariageEpouxPrenom.get()
            mariageEpouseNomInfo=entreeMariageEpouseNom.get()
            mariageEpousePrenomInfo=entreeMariageEpousePrenom.get()
            mariageInfo=()


            fenInfo.destroy() #Destruction de la fenêtre
        
        donnee=(Nom,Prenom)
        print(DateNaissance(donnee))

        print(Deces(donnee))

        print(Mariage(donnee))


        texteNomInfo=Label(fenInfo,text="Nom :") #Nom
        texteNomInfo.place(x=5,y=10) 
        entreeNomInfo=Entry(fenInfo)
        entreeNomInfo.place(x=100,y=9)
        entreeNomInfo.insert(0,donnee[0])
        textePrenomInfo=Label(fenInfo,text="Prénom :") #Prénom
        textePrenomInfo.place(x=5,y=40)
        entreePrenomInfo=Entry(fenInfo)
        entreePrenomInfo.place(x=100,y=39)
        entreePrenomInfo.insert(0,donnee[1])


        texteNaissanceDate=Label(fenInfo,text="Est né le :") #Date de Naissance
        texteNaissanceDate.place(x=5,y=70)
        entreeNaissanceDate=Entry(fenInfo)
        entreeNaissanceDate.place(x=100,y=69)
        entreeNaissanceDate.insert(0,DateNaissance(donnee)[0])
        texteNaissanceLieu=Label(fenInfo,text="à :") #Lieu de Naissance
        texteNaissanceLieu.place(x=5,y=100)
        entreeNaissanceLieu=Entry(fenInfo)
        entreeNaissanceLieu.place(x=100,y=99)
        entreeNaissanceLieu.insert(0,DateNaissance(donnee)[1])
        texteNaissanceAdresse=Label(fenInfo,text="au :") #Adresse de Naissance
        texteNaissanceAdresse.place(x=230,y=100)
        entreeNaissanceAdresse=Entry(fenInfo)
        entreeNaissanceAdresse.place(x=290,y=99)
        entreeNaissanceAdresse.insert(0,DateNaissance(donnee)[2])


        texteMariageDate=Label(fenInfo,text="Marié le :") #Date de mariage
        texteMariageDate.place(x=5,y=130)
        entreeMariageDate=Entry(fenInfo)
        entreeMariageDate.place(x=100,y=129)
        entreeMariageDate.insert(0,Mariage(donnee)[0])
        texteMariageLieu=Label(fenInfo,text="à :") #Lieu du mariage
        texteMariageLieu.place(x=230,y=130)
        entreeMariageLieu=Entry(fenInfo)
        entreeMariageLieu.place(x=290,y=129)
        entreeMariageLieu.insert(0,Mariage(donnee)[1])
        texteMariageEpouxNom=Label(fenInfo,text="Les mariés sont :") #Nom du marié 1
        texteMariageEpouxNom.place(x=5,y=160)
        entreeMariageEpouxNom=Entry(fenInfo)
        entreeMariageEpouxNom.place(x=100,y=159)
        entreeMariageEpouxNom.insert(0,Mariage(donnee)[2])
        entreeMariageEpouxPrenom=Entry(fenInfo) #Prénom du marié 1
        entreeMariageEpouxPrenom.place(x=200,y=159)
        entreeMariageEpouxPrenom.insert(0,Mariage(donnee)[3])
        texteMariageEpouseNom=Label(fenInfo,text="Marié le :") #Nom du marié 2
        texteMariageEpouseNom.place(x=5,y=190)
        entreeMariageEpouseNom=Entry(fenInfo)
        entreeMariageEpouseNom.place(x=100,y=189)
        entreeMariageEpouseNom.insert(0,Mariage(donnee)[4])
        entreeMariageEpousePrenom=Entry(fenInfo) #Prénom du marié 2
        entreeMariageEpousePrenom.place(x=200,y=189)
        entreeMariageEpousePrenom.insert(0,Mariage(donnee)[5])
        rep=0
        for instance in Enfant(donnee):
            texteEnfantNom=Label(fenInfo,text="Son enfant est :") #Enfant issu mariage
            texteEnfantNom.place(x=5,y=220+rep*30)
            entreeEnfantNom=Entry(fenInfo)
            entreeEnfantNom.place(x=100,y=219+rep*30)
            entreeEnfantNom.insert(0,instance[0])
            entreeEnfantPrenom=Entry(fenInfo) #Prénom enfant
            entreeEnfantPrenom.place(x=200,y=219+rep*30)
            entreeEnfantPrenom.insert(0,instance[1])
            rep=rep+1

        boutonValider=Button(fenInfo,text="Valider les modifications",command=Modification)
        boutonValider.config(bg='orange')
        boutonValider.place(x=150,y=350)

        Nom=rechNom
        Prenom=rechPrenom
        fenInfo.mainloop()
    else:
        print("pas dans la base")



def CreerArbre():
    '''Cette fonction permet de créer un arbre généalogique sur trois générations au dessus de la personne sélectionné'''
    global Nom,Prenom,tempNom,tempPrenom
    Canevas.delete("all") #Reset du Canevas
    if EstDedans():
        global repArbrePere,donnee
        donnee=(entreeNom.get(),entreePrenom.get())
        donneeMere=()
        racine=Canevas.create_rectangle(325,500,475,600)#Personne sélectionné
        racineTexte=Canevas.create_text(400,550,text=donnee)
        branche1=Canevas.create_rectangle(125,350,275,450)#Père
        branche2=Canevas.create_rectangle(525,350,675,450)#Mère
        branche3=Canevas.create_rectangle(25,200,175,300)#Grand-Père (Père du Père)
        branche4=Canevas.create_rectangle(225,200,375,300)#Grand-Mère (Mère du Père)
        branche5=Canevas.create_rectangle(425,200,575,300)#Grand-Père (Père de la mère)
        branche6=Canevas.create_rectangle(625,200,775,300)#Grand-Mère (Père de la mère)
        repArbrePere=0
        

        def ArbrePereRec():
            '''Cette fonction permet de créer l'arbre de gauche qui représente le père'''
            global repArbrePere,donnee,pere,mere
            connexion = sqlite3.connect("base.db")
            curseur = connexion.cursor()
            curseur.execute("SELECT Pere.Nom,Pere.Prenom,Mere.Nom,Mere.Prenom FROM Personne AS Enfant JOIN Personne AS Pere \
                            ON Enfant.Id_Pere=Pere.Id_personne JOIN Personne AS Mere ON Enfant.Id_Mere=Mere.Id_personne \
                            WHERE Enfant.Nom=? AND Enfant.Prenom=?",donnee)
            parent=curseur.fetchall()
            if parent == []:
                pereTexte=Canevas.create_text(200-100*repArbrePere,400-150*repArbrePere,text="Pas d'info")
                mereTexte=Canevas.create_text(600-repArbrePere*300,400-repArbrePere*150,text="Pas d'info")
            else :
                for instance in parent:
                    pere=[instance[0],instance[1]]
                    mere=[instance[2],instance[3]]
                pereTexte=Canevas.create_text(200-100*repArbrePere,400-150*repArbrePere,text=pere[0]+" "+pere[1])
                mereTexte=Canevas.create_text(600-repArbrePere*300,400-repArbrePere*150,text=mere[0]+" "+mere[1])
            donnee=(pere[0],pere[1])
            repArbrePere=repArbrePere+1
            donneeMere=(mere[0],mere[1])
            connexion.commit()
            connexion.close()
            return (donneeMere)
            
        
        def ArbreMereRec(donneeMere):
            '''Cette fonction permet de créer l'arbre de droite qui représente la mère avec comme donnée le fils'''
            global pere,mere
            connexion = sqlite3.connect("base.db")
            curseur = connexion.cursor()
            curseur.execute("SELECT Pere.Nom,Pere.Prenom,Mere.Nom,Mere.Prenom FROM Personne AS Enfant JOIN Personne AS Pere \
                            ON Enfant.Id_Pere=Pere.Id_personne JOIN Personne AS Mere ON Enfant.Id_Mere=Mere.Id_personne \
                            WHERE Enfant.Nom=? AND Enfant.Prenom=?",donneeMere)
            parent=curseur.fetchall()
            if parent == []:
                pereTexte=Canevas.create_text(500,200,text="Pas d'info")
                mereTexte=Canevas.create_text(700,250,text="Pas d'info")                
            else :
                for instance in parent:
                    pere=[instance[0],instance[1]]
                    mere=[instance[2],instance[3]]
                pereTexte=Canevas.create_text(500,250,text=pere[0]+" "+pere[1])
                mereTexte=Canevas.create_text(700,250,text=mere[0]+" "+mere[1])
            connexion.commit()
            connexion.close()

        while repArbrePere!=1 :
            ArbreMereRec(ArbrePereRec())
            fin= True
        if fin is True:
            ArbrePereRec()

def clicG(event):
    '''Cette fonction permet de définir ce que fait un clic selon la position du pointeur de la souris'''
    global donnee,Nom,Prenom,rechNom,rechPrenom
    Nom=entreeNom.get()
    Prenom=entreePrenom.get()
    rechNom=Nom
    rechPrenom=Prenom
    donnee=(rechNom,rechPrenom)
    if 325<event.x<475 and 500<event.y<600: #Racine
        Recherche()
    if 125<event.x<275 and 350<event.y<450: #Père
        connexion = sqlite3.connect("base.db")
        curseur = connexion.cursor()
        curseur.execute("SELECT Pere.Nom,Pere.Prenom FROM Personne AS Enfant JOIN Personne AS Pere \
                        ON Enfant.Id_Pere=Pere.Id_personne WHERE Enfant.Nom=? AND Enfant.Prenom=?",donnee)
        donneeRecherche=curseur.fetchall()
        for instance in donneeRecherche:
            Nom=instance[0]
            Prenom=instance[1]
        connexion.commit()
        connexion.close()
        if donneeRecherche==[]:
            Ajouter("père")
        else:
            Recherche()
    if 525<event.x<675 and 350<event.y<450: #Mère
        connexion = sqlite3.connect("base.db")
        curseur = connexion.cursor()
        curseur.execute("SELECT Mere.Nom,Mere.Prenom FROM Personne AS Enfant JOIN Personne AS Mere \
                        ON Enfant.Id_Mere=Mere.Id_personne WHERE Enfant.Nom=? AND Enfant.Prenom=?",donnee)
        donneeRecherche=curseur.fetchall()
        for instance in donneeRecherche:
            Nom=instance[0]
            Prenom=instance[1]
        connexion.commit()
        connexion.close()
        if donneeRecherche==[]:
            Ajouter("mère")
        else:
            Recherche()
    if 25<event.x<175 and 200<event.y<300: #Grand-Père (Père du Père)
        connexion = sqlite3.connect("base.db")
        curseur = connexion.cursor()
        curseur.execute("SELECT GrandPere.Nom,GrandPere.Prenom FROM Personne AS Enfant JOIN Personne AS Pere \
                        ON Enfant.Id_Pere=Pere.Id_personne Join Personne AS GrandPere ON Pere.Id_Pere=GrandPere.Id_personne \
                        WHERE Enfant.Nom=? AND Enfant.Prenom=?",donnee)
        donneeRecherche=curseur.fetchall()
        for instance in donneeRecherche:
            Nom=instance[0]
            Prenom=instance[1]
        connexion.commit()
        connexion.close()
        if donneeRecherche==[]:
            Ajouter("père")
        else:
            Recherche()
    if 225<event.x<375 and 200<event.y<300: #Grand-Mère (Mère du Père)
        connexion = sqlite3.connect("base.db")
        curseur = connexion.cursor()
        curseur.execute("SELECT GrandMere.Nom,GrandMere.Prenom FROM Personne AS Enfant JOIN Personne AS Pere \
                        ON Enfant.Id_Pere=Pere.Id_personne Join Personne AS GrandMere ON Pere.Id_Mere=GrandMere.Id_personne \
                        WHERE Enfant.Nom=? AND Enfant.Prenom=?",donnee)
        donneeRecherche=curseur.fetchall()
        for instance in donneeRecherche:
            Nom=instance[0]
            Prenom=instance[1]
        connexion.commit()
        connexion.close()
        if donneeRecherche==[]:
            Ajouter("mère")
        else:
            Recherche()
    if 425<event.x<575 and 200<event.y<300: #Grand-Père (Père de la Mère)
        connexion = sqlite3.connect("base.db")
        curseur = connexion.cursor()
        curseur.execute("SELECT GrandPere.Nom,GrandPere.Prenom FROM Personne AS Enfant JOIN Personne AS Mere \
                        ON Enfant.Id_Mere=Mere.Id_personne Join Personne AS GrandPere ON Mere.Id_Pere=GrandPere.Id_personne \
                        WHERE Enfant.Nom=? AND Enfant.Prenom=?",donnee)
        donneeRecherche=curseur.fetchall()
        for instance in donneeRecherche:
            Nom=instance[0]
            Prenom=instance[1]
        connexion.commit()
        connexion.close()
        if donneeRecherche==[]:
            Ajouter("père")
        else:
            Recherche()
    if 625<event.x<775 and 200<event.y<300: #Grand-Mère (Mère de la Mère)
        connexion = sqlite3.connect("base.db")
        curseur = connexion.cursor()
        curseur.execute("SELECT GrandMere.Nom,GrandMere.Prenom FROM Personne AS Enfant JOIN Personne AS Mere \
                        ON Enfant.Id_Mere=Mere.Id_personne Join Personne AS GrandMere ON Mere.Id_Mere=GrandMere.Id_personne \
                        WHERE Enfant.Nom=? AND Enfant.Prenom=?",donnee)
        donneeRecherche=curseur.fetchall()
        for instance in donneeRecherche:
            Nom=instance[0]
            Prenom=instance[1]
        connexion.commit()
        connexion.close()
        if donneeRecherche==[]:
            Ajouter("mère")
        else:
            Recherche()

#Création du Canevas
Canevas=Canvas(fenetre,width=800,height=650)
Canevas.place(x=0,y=0)

choixNom = Label(fenetre, text="Entrez votre nom ici :") 
choixNom.place(x=0,y=25)

entreeNom = Entry(fenetre)
entreeNom.place(x=175,y=25)

choixPrenom = Label(fenetre, text="Entrez votre prenom ici :")
choixPrenom.place(x=0,y=75)

entreePrenom = Entry(fenetre)
entreePrenom.place(x=175,y=75)

boutonRecherche = Button(fenetre, text="Recherche", command=Recherche) #Bouton Recherche
boutonRecherche.config(bg='orange')
boutonRecherche.place(x=450,y=35)

boutonCreationArbre = Button(fenetre, text="Créer un arbre", command=CreerArbre) #Bouton de création d'arbre
boutonCreationArbre.config(bg='orange')
boutonCreationArbre.place(x=550,y=35)


fenetre.bind('<Button-1>', clicG) #Définition de l'action clicG
fenetre.mainloop()