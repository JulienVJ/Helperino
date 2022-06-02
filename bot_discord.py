import discord
from discord.ext import commands
import random
from movieTab import movieTab
from realMovieTab import realMovieTab
from Fouras import guess_table

client = discord.Client()

client = commands.Bot(command_prefix="!")

#Création du node pour l'arbre

class Node :
    def __init__(self, question, keyword, list_child):
        self.question = question
        self.keyword = keyword
        self.list_child = list_child

#Fonction pour ajouter un enfant ou injecter une branche
    def insert_node(self, node, question):
        if self.question == question :
            self.list_child.append(node)

        for Node_child in self.list_child:
            Node_child.insert_node(node,question)
            
     
#Création de l'arbre
Root = Node("Que recherchez-vous ?","Helperino",[])
Root.insert_node(Node("Jouons à un petit jeu","Père Fouras",[]),"Que recherchez-vous ?")
Root.insert_node(Node("De quel réalisateur veux-tu un film ?","Réalisateur",[]),"Que recherchez-vous ?")
Root.insert_node(Node("Un film avant ou après les années 2000 ?","Film",[]),"Que recherchez-vous ?")
Root.insert_node(Node("Voici les commandes disponibles que je pourrai comprendre et interagir avec : Film, Réalisateur, Père Fouras, Reload (pour charger un nouveau film lorsque Film est sélectionné), Reset (pour revenir au début). Veuillez me Reset et me rappeler afin que je puisse vous aider !","Aide",[]),"Que recherchez-vous ?")


Root.insert_node(Node("Voici un film de Luc Besson","Luc Besson",[]),"De quel réalisateur veux-tu un film ?")
Root.insert_node(Node("Voici un film de Steven Spielberg","Steven Spielberg",[]),"De quel réalisateur veux-tu un film ?")
Root.insert_node(Node("Voici un film de Quentin Tarantino","Quentin Tarantino",[]),"De quel réalisateur veux-tu un film ?")
Root.insert_node(Node("Voici un film de Clint EastWood","Clint EastWood",[]),"De quel réalisateur veux-tu un film ?")
Root.insert_node(Node("Voici un film de Christopher Nolan","Christopher Nolan",[]),"De quel réalisateur veux-tu un film ?") 


Root.insert_node(Node("La réponse était Scream !","Scream",[]),"Jouons à un petit jeu")
Root.insert_node(Node("C'est la voiture de Retour vers le futur !","Retour vers le futur",[]),"Jouons à un petit jeu")
Root.insert_node(Node("Cette citation provient du film 300 !","300",[]),"Jouons à un petit jeu")
Root.insert_node(Node("Cette musique est le thème musical principal de Pirates des Caraïbes !","Pirates des caraïbes",[]),"Jouons à un petit jeu")
Root.insert_node(Node("C'est l'intrigue du film Alien !","Alien",[]),"Jouons à un petit jeu")


Root.insert_node(Node("Quelle catégorie veux-tu voir ?","Avant",[]),"Un film avant ou après les années 2000 ?")
Root.insert_node(Node("Quelle catégorie veux-tu voir ?","Après",[]),"Un film avant ou après les années 2000 ?")


Root.insert_node(Node("Voici votre film","Horreur",[]),"Quelle catégorie veux-tu voir ?")
Root.insert_node(Node("Voici votre film","SF",[]),"Quelle catégorie veux-tu voir ?")
Root.insert_node(Node("Voici votre film","Action",[]),"Quelle catégorie veux-tu voir ?")


Root.insert_node(Node("Réalisé par","Real",[]),"Voici votre film")
Root.insert_node(Node("Réalisé le","Date",[]),"Voici votre film")
Root.insert_node(Node("Synopsis","Synopsis",[]),"Voici votre film")

#Variables globales du node actuel
currentNode = Root
Before = False
After = False
tabCurrent = []

#Fonction qui return un film d'un réalisateur choisi
def random_movies_real (tab=realMovieTab, txt=""):
    test1 = random.randint(1,10)
    if txt == "Luc Besson":
        return tab["Luc Besson"][test1]
    elif txt == "Steven Spielberg":
        return tab["Steven Spielberg"][test1]
    elif txt == "Quentin Tarantino":
        return tab["Quentin Tarantino"][test1]
    elif txt == "Clint Eastwood":
        return tab["Clint Eastwood"][test1]
    elif txt == "Christopher Nolan":
        return tab["Christopher Nolan"][test1]

#Fonction qui return un film d'une catégorie choisie
def random_movies (tab=movieTab, txt="", Before=Before, After=After):
    nbrRandom = random.randint(1,10)
    if Before == True:
        if txt == "Horreur":
            return tab["Avant"]["Horreur"][nbrRandom]
        elif txt == "SF":
            return tab["Avant"]["SF"][nbrRandom]
        elif txt == "Action":
            return tab["Avant"]["Action"][nbrRandom]
    elif After == True:
        if txt == "Horreur":
            return tab["Après"]["Horreur"][nbrRandom]
        elif txt == "SF":
            return tab["Après"]["SF"][nbrRandom]
        elif txt == "Action":
            return tab["Après"]["Action"][nbrRandom]


F = False
R = False
#Fonction event réagissant à chaque message
@client.event
async def on_message (message) :
#Instanciation des variables en global
    global currentNode 
    global Before
    global After
    global movieTab
    global Root
    global realMovieTab
    global F
    global R
    global tabCurrent
    global number
#Mise en place du reset du bot
    if message.content == "Reset":
        currentNode = Root
        Before = False
        After = False
        F = False
        R = False
        tabCurrent.clear()
#Mise en place du reload d'un film de réal ou de catégorie
    elif message.content == "Reload":
        if F == True:
            test = random_movies(movieTab ,currentNode.keyword,Before, After)
            await message.channel.send(test[0])
            await message.channel.send(test[1])
        elif R == True:
            test = random_movies_real(realMovieTab ,currentNode.keyword)
            await message.channel.send(test)
#Retour en arrière section film
    elif message.content == "Back":
        currentNode = tabCurrent[2]
#Affiche la réponse du bot
    elif message.content == currentNode.keyword:
            await message.channel.send(currentNode.question)
#Verification si c'est la bonne réponse pour l'énigme du Père Fouras
    if currentNode.keyword == "Père Fouras":
        if guess_table[number][0] == message.content :
            await message.channel.send("Vous avez la bonne réponse !")
        else:
            return    
#Parcours l'arbre en fonction du messagede l'utilisateur pour envoyer la réponse du bot     
    else:
        for child in currentNode.list_child:
            if child.keyword in message.content:
                currentNode = child
                tabCurrent.append(child)
                await message.channel.send(currentNode.question)
                
                if message.content == "Avant":
                    Before = True
                elif message.content == "Après":
                    After = True
                elif message.content == "Film":
                    F = True
                elif message.content == "Réalisateur":
                    R = True 
#Permet d'envoyer le film sur le chat en appelant la fonction d'envoi 
                if F == True:
                    test = random_movies(movieTab ,currentNode.keyword,Before, After)
                    await message.channel.send(test[0])
                    await message.channel.send(test[1])
                elif R == True:
                    test = random_movies_real(realMovieTab ,currentNode.keyword)
                    await message.channel.send(test)
#Création de l'énigme 
    if message.content == "Père Fouras":
        number = random.randint(1,5)
        await message.channel.send(guess_table[number][1])
        if number == 4:
            await message.channel.send(file = discord.File("Audio_mystere.mp3"))
        else :
            await message.channel.send(guess_table[number][2])
#Relier le bot au discord où il est intégré
client.run("OTc4MjI4OTAxMDIzMTg2OTY0.GVDnvh._RMIJwDqzwcJixUsjuXrAfM_mwHk9KsKoCA1EQ")
