import tkinter as tk
from tkinter import *
import json


class score(object):
    def __init__(self, nom_joueur, nb_point):
        self.nom_joueur=nom_joueur
        self.nb_point=nb_point
  
    def toFile(self, fichier):
        f = open(fichier,"w")
        s=self
        json.dump(s.__dict__,f)
        f.close()
        
    
    def fromFile(cls, fichier):
        f = open(fichier,"r")
        d = json.load(f)
        snew=score(d["nom_joueur"],d["nb_point"])
        f.close()
        return snew
    
    def __str__(self):
         return str(self.nom_joueur) + ',' +str(self.nb_point)
        

class resultat(object):
    def __init__(self):
        self.lesscores=[]
    def ajout(self, score):
        self.lesscores.append(score)
    def __str__(self):
        chaine=str(self.lesscores[0])
        for e in self.lesscores[1:]:
            chaine=chaine+ "," + str(e)
        return chaine
    

    def fromFile(cls,fichier):
        f = open(fichier,"r")
        #chargement
        tmp = json.load(f)
        
        liste = []
        for d in tmp:
            #créer un livre
            s=score(d["nom_joueur"],d["nb_point"])
            #l'ajouter dans la liste
            liste.append(s)
        res=resultat()
        res.lesscores=liste
        f.close();
        return res
    
    def toFile(self,fichier):
        f = open(fichier,"w")
        tmp = []
        for s in self.lesscores:
        #créer un dictionnaire
            d = {}
            d["nom_joueur"] = s.nom_joueur
            d["nb_point"] = s.nb_point       
            tmp.append(d)
        json.dump(tmp,f)
        f.close();

      #------commentaires------:
# Class Defender : 
# le deplacement du defender
# fonction fire pour controler le nombre autorise de bullet
# fonction move_bullet pour controler le deplacement du bullet 
class Defender(object):
    def __init__(self): 
        self.width = 20
        self.height = 45
        self.move_delta = 10 
        self.id = None
        self.max_fired_bullets = 2
        self.fired_bullets = []
        self.canvas_height = Fleet().get_height()
        self.canvas_width = Fleet().get_width()
        self.dx = self.canvas_width//2 - self.width//2
        self.dy = self.canvas_height - self.height        

    def get_id(self):
        return self.id
    def get_fire(self):
        return self.fired_bullets
    def set_fire(self,liste):
        self.fired_bullets=liste
    def get_dx(self):
        return self.dx
    def get_dy(self):
        return self.dy
    def set_dx(self,valeurx):
        self.dx=valeurx
    def set_dy(self,valeury):
        self.dy=valeury
        
    def install_in(self, canvas):
        self.canvas=canvas
        lx = self.get_dx()
        ly = self.get_dy()
        self.rectangle = canvas.create_rectangle(lx, ly, lx + self.width, ly + self.height, fill="green")
        
        
    def bunkers(self,canvas):
        global Liste,Coordonneescarre       
        Liste=[]
        Coordonneescarre=[]
        i=0
        x=100
        y=450
        while i<3: # pour creer 3 bunkers
            Xmax=x+120
            Ymax=y+60
            departx=x
            while y<Ymax:
                while x<Xmax:
                    Liste.append(canvas.create_rectangle(x,y,x+20,y+20,fill='grey'))
                    Coordonneescarre.append([x,y])
                    x+=20
                x=departx
                y+=20
            i+=1
            x+=220
            y-=60
        
    def keypress(self, event):
        x = 0
        xn=self.get_dx()  
        if event.keysym == 'Left':
            if xn > 0:   
                self.set_dx(self.get_dx()-self.move_delta)    
                self.move_in(self.canvas,-self.move_delta)     
        elif event.keysym == 'Right':
            if xn+self.move_delta < self.canvas_width:   
                self.set_dx(self.get_dx()+self.move_delta)   
                self.move_in(self.canvas,self.move_delta)     
        elif event.keysym == 'space':  
            self.id = 1
            self.bullet = Bullet(self.id)
            self.bullet.set_xb(self.get_dx())    
            self.bullet.set_yb(self.get_dy())
            self.fire(self.canvas)
        
    def move_in(self,canvas, dx): 
        canvas.move(self.rectangle, dx, 0)
       
    def fire(self, canvas):
        if len(self.get_fire()) < self.max_fired_bullets:     
            self.bullet.id = self.bullet.install_in(self.canvas)    
            self.fired_bullets.append(self.bullet.id) 
    
    def move_bullet(self,canvas):
        for i in range(0,len(self.fired_bullets)):
            x1,y1,x2,y2 = self.canvas.bbox(self.fired_bullets[i])
            if y1<0:    
                canvas.delete(self.fired_bullets[i])    
                del self.fired_bullets[i]   
                break
            else:
                self.bullet.move_in(self.canvas,self.fired_bullets[i])  
                
        #------commentaires------:
#creation du bullet 
class Bullet(object):
    def __init__(self, shooter):
        self.radius = 15
        self.color = "yellow"
        self.speed = 35
        self.id = None
        self.shooter = shooter
        self.x=Defender().get_dx()
        self.y=Defender().get_dy()
    def get_id(self):
        return self.id
    def set_id(self,bid): 
        self.id = bid
    def get_xb(self):      
        return self.xb
    def get_yb(self):
        return self.yb
    def set_xb(self,valeurx):
        self.xb=valeurx
    def set_yb(self,valeury):
        self.yb=valeury
        
    def install_in(self, canvas):
        lx = self.get_xb() + 5
        ly = self.get_yb() - 10
        self.id = canvas.create_oval(lx, ly, lx + self.radius, ly + self.radius, fill=self.color)
        return self.id
    
    def move_in(self,canvas,ovale):
        self.id=ovale
        canvas.move(self.id, 0, -self.speed)

        
class Fleet(object):
    def __init__(self):
        self.aliens_lines = 4
        self.aliens_columns = 6
        self.aliens_inner_gap = 30
        self.alien_x_delta = 5
        self.alien_y_delta = 10
        fleet_size = self.aliens_lines * self.aliens_columns
        self.aliens_fleet = [None] * fleet_size
        self.width = 700
        self.height =600
    
    def get_fx(self):
        return self.alien_x_delta
    def get_fy(self):
        return self.alien_y_delta
    def set_fx(self,fx):
        self.alien_x_delta=fx
    def get_width(self):
        return self.width
    def get_height(self):
        return self.height
    
    def get_score(self):
        return (self.aliens_lines * self.aliens_columns - len(self.aliens_fleet))*20   
    def install_in(self, canvas):
        self.alien=Alien()
        self.canvas=canvas
        self.x=50  
        self.y=50
        position=0 
        
        for i in range(0,self.aliens_lines):
            for j in range(0,self.aliens_columns):
                self.aliens_fleet[position] = self.alien.install_in(self.canvas,self.x,self.y)
                position+=1
                self.x += self.aliens_inner_gap+73  
            self.x=50
            self.y += self.aliens_inner_gap+53  
           
    def move_in(self, canvas): 
        if len(self.aliens_fleet)!=0:
            all_rect_ids = self.canvas.find_withtag("alien")
            x1,y1,x2,y2 = self.canvas.bbox("alien")
            
            if x2>=700:      
                self.set_fx(-self.get_fx())
                fy = self.alien_y_delta
            elif x1<=0:      
                self.set_fx(-self.get_fx())
                fy = self.alien_y_delta
            else:       
                fy=0

            for i in range(0,len(all_rect_ids)):
                self.alien.move_in(self.canvas,all_rect_ids[i],self.alien_x_delta,fy)
                
     #---------commentaires-----:
# dans fonction on va faire le conditions suivantes:
# si des aliens vivants existent
# est ce que le bullet a toucher un alien 
# ensuite on va suprimer le bullet et l'alien 

    def fonction(self,canvas,defender):
        self.canvas=canvas
        self.defender=defender
        
        for i in range(len(self.defender.fired_bullets)):
            cond_sorti=0   
#coordonnes des bullets
            xb1,yb1,xb2,yb2=self.canvas.bbox(self.defender.fired_bullets[i]) 
            for j in range(len(self.aliens_fleet)):
    
                if self.aliens_fleet[j] != None: 
                    xa1,ya1,xa2,ya2=self.canvas.bbox(self.aliens_fleet[j])

                    if (xb1>=xa1 or xb2>=xa1) and (xb1<=xa2 or xb2<=xa2) and yb1<=ya2 and yb1>=ya1:
                        self.alien.expo(self.canvas,self.defender.fired_bullets[i]) 
                        canvas.delete(self.defender.fired_bullets[i])  
                        canvas.delete(self.aliens_fleet[j])    
                        self.alien.alive = False
      
                        del self.defender.fired_bullets[i]   
                        del self.aliens_fleet[j] 
                        cond_sorti=1    
                        break
                        
            if(cond_sorti==1):
                break     
                
        #-----------commentaires----------:                
 #dans cette class on a :
 # la creation d'un alien 
 # le deplacement de l'alien 
 # creer l'explosion
class Alien(object):
    def __init__(self):
        self.id = None
        self.alive = True
        self.alien = PhotoImage(file="alien.gif")
        self.explosion = PhotoImage(file="explosion.gif")
 
    def install_in(self, canvas, x, y):  
        self.id = canvas.create_image(x, y, image=self.alien, tags="alien")
        return self.id
    
    def move_in(self, canvas, alien, dx, dy):
        self.id=alien
        canvas.move(self.id, dx, dy)

    def expo(self,canvas,projectile):
        xa1,ya1,xa2,ya2=canvas.bbox(projectile)
        explosion = canvas.create_image(xa1+(xa2-xa1)/2, ya1+(ya2-ya1)/2, image=self.explosion, tags="explosion")
        canvas.after(100,canvas.delete,explosion)        
        
    

class Game(object):
    
    global xe,ye,xe2,ye2,xe3,ye3,LimiteAvancement,dx,ListeCoordEnnemis,ListeEnnemis,ObusEnnemi,flag,photo,NbreEnnemis,Score,ViesJoueur
    global ListeAbri,CoordonneesBriques,projectile,feu,feuEnnemi,PasAvancement
    global dyobus,dyobusEnnemi,DebutJeu,BonusActif,dxeb,EnnemiBonus,Mort,photo,PasMax,NbreEnRangees
    
    def Creation_CanonMobile():
        global canon, xc1, xc2, yc1, yc2
        canon=[]

        xc1=20
        yc1=440

        # Création du canon

        canon.append(can.create_rectangle(xc1,yc1,xc1+20,yc1+20,fill='green'))

        xc2=xc1-20
        yc2=yc1+20

        # Création de la plate-forme du canon

        canon.append(can.create_rectangle(xc2,yc2,xc2+60,yc2+20,fill='green'))
    
    def __init__(self, frame):
        width=700
        height=600
        self.frame=frame
        self.canvas=tk.Canvas(self.frame,width=width, height=height,bg="black")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.fleet=Fleet()
        self.defender=Defender()
        self.defender.install_in(self.canvas)
        self.fleet.install_in(self.canvas)
        self.defender.bunkers(self.canvas)
       
    def start_animation(self):
        self.animation()

    def animation(self):
        self.score = StringVar()  #score actuel
        label = Label(self.canvas, textvariable = self.score)
        self.score.set("score : " + str(self.fleet.get_score())) 
        self.canvas.create_window(40, 50, window = label)
        self.move_bullets()
        self.move_aliens_fleet()
        self.fleet.fonction(self.canvas,self.defender)
        self.canvas.after(100,self.animation)

    def move_bullets(self):
        if self.defender.get_id() == 1:
            self.defender.move_bullet(self.canvas)
            
    def move_aliens_fleet(self):
        self.fleet.move_in(self.canvas)          
           
                        
class SpaceInvaders(object): 
   
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Space Invaders")
        width=700
        height=600
        self.frame=tk.Frame(self.root,width=width, height=height,bg="green")
        self.frame.pack()
        self.game = Game(self.frame)
        
    def play(self): 
        self.game.start_animation()
        self.root.bind("<Key>", self.game.defender.keypress)
        self.root.mainloop()        
                
        
                
jeu=SpaceInvaders()
jeu.play()