import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button, ButtonBehavior
from kivy.properties import (NumericProperty, ReferenceListProperty,
    ObjectProperty, StringProperty, ListProperty)
from kivy.clock import Clock
import time
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from datetime import datetime, timedelta
import queue
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from kivy.lang import Builder


class JumpingApp(App):
    def build(self):
        game = JumpingGame()
        Clock.schedule_interval(game.update, 1.0/60.0)
        Clock.schedule_once(game.init_game)
        return game




class JumpingXp(FloatLayout):
    position = (Window.size[0]/2,0)
    direction = (0,0)
    v_bild = StringProperty("xp.png")
    groesse = [Window.size[0]/5,Window.size[0]/5]
    def move(self):
        self.pos=go(JumpingXp)
    def animation(self):
        if round(datetime.now().timestamp()*3)%2==0:
            self.v_bild = "xp2.png"
        else:
            self.v_bild="xp.png"

class JumpingGame(Widget):
    xp = JumpingXp()
    trampoline = ObjectProperty(None)
    button = ObjectProperty(None)
    guy = ObjectProperty(None)
    buildings = ObjectProperty(None)
    showlevel = ObjectProperty(None)
    showlevelbackground = ObjectProperty(None)
    progress = ObjectProperty(None)
    progressbackground = ObjectProperty(None)
    anzeige = ObjectProperty(None)
    pfeil = ObjectProperty(None)
    shopbutton = ObjectProperty(None)
    shop = ObjectProperty(None)
    universe = ObjectProperty(None)
    highscore = ObjectProperty(None)
    xp_places = [2157,3500,5477,7317,10157,15000,20077,25017,110211021102]
    status = "Wait"
    cordinates = queue.Queue()
    store = JsonStore("stats.json")
    if not store.exists("Stats"):
        store.put("Stats", level=0.4, trampoline = "trampolin1.png", points = [65,70,66,70])
    if not store.exists("High"):
        store.put("High", highscore=1000)
    level = float(store.get("Stats")["level"])
    tr = store.get("Stats")["trampoline"]
    points = store.get("Stats")["points"]
    high = store.get("High")["highscore"]
    def init_game(self, dt):
        JumpingGuy.level = self.store.get("Stats")["level"]
        self.trampoline.source = self.store.get("Stats")["trampoline"]
        self.progress.points = self.store.get("Stats")["points"]
        self.highscore.text = "Highscore {}".format(int(self.store.get("High")["highscore"]))
        self.showlevel.set_text()
        self.guy.move()
        self.buildings.move()
        self.trampoline.move()
        self.xp.move()
        self.xp.animation()
        self.shopbutton.move()
        self.shop.move()
        self.button.move()
        self.highscore.move()
    def update(self, dt):
        self.status = JumpingGame.status
        if self.status != "Wait":
            self.guy.move()
            self.buildings.move()
            self.trampoline.move()
            self.xp.move()
            self.xp.animation()
            self.highscore.move()
        else:
            self.pfeil.move()  
        if self.status == "FlyUp" or self.status == "Stop":
            if JumpingGuy.position[1]>=250:
                JumpingGuy.direction = (0,0)
            if JumpingGame.status == "Stop":
                global i
                i = i + 1
                JumpingTrampoline.direction = (0,i/100)
                JumpingBuildings.direction = (0,i/100)
                JumpingXp.direction = (0,i/100)
                if i == -50:
                    self.guy.bild = "Typ.png"
                if i == 0:
                    self.button.ids["red_button"].source = "button2.png"
                    JumpingGame.status = "DownAgain"
                    self.status = JumpingGame.status
            for cordinate in self.xp_places:
                if (cordinate-100<((-JumpingBuildings.position[1])+
                                   JumpingGuy.position[1])<cordinate+100):
                    wert=self.cordinates.get()
                    if cordinate == wert:
                        self.progress.wachsen(3/(JumpingGuy.level*8.5-3))
                        self.xp.ids["x{}".format(cordinate)].opacity = 0##########
                    else:
                        self.cordinates.put(wert)
                    
        if self.status == "FlyDown" and (JumpingGuy.position[1]<
                JumpingTrampoline.position[1]+100):
            JumpingGuy.direction = (0,0.08)
            self.guy.flying_since=0
            JumpingTrampoline.direction=(0,-2)
            JumpingBuildings.direction=(0,-2)
            JumpingXp.direction=(0,-2)
            if self.pfeil.wert() == 0.1:
                self.guy.bild = "Typ schnell.png"
            else:
                self.guy.bild = "Typ normal.png"
            self.cordinates = queue.Queue()
            for cordinate in self.xp_places:
                self.cordinates.put(cordinate)
            self.status = "FlyUp"
            JumpingGame.status = self.status

        if (JumpingGame.status == "FlyDownAgain" and
            JumpingTrampoline.position[1]>=0):
                JumpingTrampoline.direction = (0,0)
                JumpingBuildings.direction = (0,0)
                JumpingXp.direction = (0,0)
                JumpingGuy.position = (Window.size[0]/2,400)
                JumpingTrampoline.position=(Window.size[0]/2-100,0)
                JumpingBuildings.position=(0,0)
                JumpingXp.position=(Window.size[0]/2,0)
                self.showlevel.opacity = 1
                self.shopbutton.opacity = 1
                self.showlevelbackground.opacity = 1
                self.guy.move()
                self.buildings.move()
                self.trampoline.move()
                self.xp.move()
                self.xp.animation()
                if JumpingPfeil.nach == "rechts":
                    JumpingPfeil.direction = (2,0)
                elif JumpingPfeil.nach == "links":
                    JumpingPfeil.direction = (-2,0)
                self.button.ids["red_button"].source="button.png"
                for xp_point in self.xp.ids:
                    self.xp.ids[xp_point].opacity = 1
                if self.store.get("High")["highscore"] != self.high:
                    self.high = self.high+50
                    self.store.put("High", highscore=self.high)
                JumpingGame.status="Wait"
                self.status = JumpingGame.status
                

    def button_on_press(self):
        if self.button.ids["red_button"].source == "button.png":
            self.button.ids["red_button"].source = "buttonp.png"
        elif self.button.ids["red_button"].source == "button2.png":
            self.button.ids["red_button"].source = "button2p.png"
        if self.shop.opacity == 1:
            self.shop.opacity = 0
        if JumpingGame.status == "Wait":
            self.shopbutton.opacity = 0
            self.showlevel.opacity = 0
            self.showlevelbackground.opacity = 0
            JumpingGuy.direction = (0,-2)
            JumpingPfeil.direction=(0,0)
            self.status = "FlyDown"
            JumpingGame.status = self.status
        if JumpingGame.status == "DownAgain":
            JumpingBuildings.direction=(0,self.guy.level+6)
            JumpingTrampoline.direction=(0,self.guy.level+6)
            JumpingXp.direction=(0,self.guy.level+6)
            self.status = "FlyDownAgain"
            JumpingGame.status = self.status
        

def go(self):
    self.position = (self.position[0]+ JumpingGuy.speed*self.direction[0],
        self.position[1]+ JumpingGuy.speed*self.direction[1])
    return self.position 


class JumpingButton(ButtonBehavior, Widget):
    def move(self):
        self.pos=(Window.size[0]-self.size[0],(Window.size[1]/2-self.parent.shop.v_size[1]/2)-self.size[0])
    def on_release(self):
        if self.ids["red_button"].source == "buttonp.png":
            self.ids["red_button"].source = "button.png"
        elif self.ids["red_button"].source == "button2p.png":
            self.ids["red_button"].source = "button2.png"

class JumpingHighscore(Widget):
    position = ListProperty([0,Window.size[1]+50])
    points = ListProperty([0,Window.size[1]+10,Window.size[0],Window.size[1]+10])
    color = ListProperty([1,1,1,1])
    text = StringProperty("Highscore {}".format(1000))
    def move(self):
        if self.parent.status != "wait" and self.parent.status != "FlyDownAgain":
            pos_on_screen = self.parent.buildings.pos[1]+self.parent.high+self.parent.guy.pos[1]+150
            if(pos_on_screen<=Window.size[1]):  
                if(pos_on_screen<=self.parent.guy.pos[1]+150):
                    if self.color == [1,1,1,1]:
                        self.color = [0,1,0,1]
                    self.position = [0,self.parent.guy.pos[1]+150]
                    self.parent.high = (-self.parent.buildings.pos[1])
                    self.text = "Highscore {}".format(int(self.parent.high))
                else:
                    self.position = [0,pos_on_screen]
        else:
            self.position = [0, Window.size[1]+50]
            self.color = [1,1,1,1]
        self.points = [0,self.position[1],Window.size[0],self.position[1]]

class JumpingShop(GridLayout):
    opacity = NumericProperty(0)
    v_size= ListProperty((Window.size[0],Window.size[0]))
    
    def move(self):
        self.v_size = (Window.size[0], Window.size[0])
    def clicked(self, str_id):
        if self.opacity == 1:
            picture = self.ids[str_id].source
            if picture != "Schloss.png":
                self.parent.trampoline.source = picture
                self.parent.store.put("Stats", level=self.parent.level, trampoline = picture, points = self.parent.points)
                self.parent.tr = picture
        elif self.opacity == 0:
            return None
    def open(self):
        for button in self.ids:
            if int(button[2:])<= (int(JumpingGuy.level*10)-3):
                self.ids[button].source="trampolin{}.png".format(button[2:])
            else:
                self.ids[button].source="Schloss.png"


class JumpingShopbutton(Button):
    source = StringProperty("shop.png")
    bild = StringProperty("trampolin1.png")
    def move(self):
        self.pos = (50, Window.size[1]-200)
    def open_shop(self):
        if self.opacity == 1:
            if self.parent.shop.opacity == 0:
                if self.source == "shop_new.png":
                    self.source = "shop.png"
                self.parent.shop.opacity = 1
                self.parent.shop.open()
            else:
                self.parent.shop.opacity = 0
                


class JumpingAnzeige(Widget):
    pos=(Window.size[0]/2-15,0)

class JumpingProgressbackground(Widget):
    pass

class JumpingProgress(Widget):
    laenge = NumericProperty(10)
    points = ListProperty([65,70,66,70])
    def wachsen(self, wert):
        points = self.points
        if points[-2]+wert>=135:
            points = [65,70,66,70]
            JumpingGuy.level = JumpingGuy.level+0.1
            self.parent.store.put("Stats", level=JumpingGuy.level, trampoline = self.parent.tr, points = self.parent.points)
            self.parent.level = JumpingGuy.level
            self.parent.shopbutton.source = "shop_new.png"
            self.parent.showlevel.set_text()
        else:
            new_max = self.points[-2]+wert
            if len(points) > 4:
                points = [65,70,66,70]
            points.append(new_max)
            points.append(70)
        self.parent.store.put("Stats", level= self.parent.level, trampoline = self.parent.tr, points= points)
        self.parent.points = points
        self.points = points

class JumpingPfeil(Widget):
    position=(Window.size[0]/2+75,-5)
    direction=(2,0)
    nach = "rechts"
    def move(self):
        if (JumpingPfeil.nach == "rechts" and
            JumpingPfeil.position[0]>=Window.size[0]/2+155 and###org:135
            JumpingPfeil.direction!=(0,0)):
            JumpingPfeil.direction=(-2,0)
            JumpingPfeil.nach = "links"
        elif (JumpingPfeil.nach == "links" and
              JumpingPfeil.position[0]<=Window.size[0]/2-25 and
              JumpingPfeil.direction!=(0,0)):
            JumpingPfeil.direction=(2,0)
            JumpingPfeil.nach="rechts"
        JumpingPfeil.position=(JumpingPfeil.position[0]+JumpingPfeil.direction[0],
                               JumpingPfeil.position[1]+JumpingPfeil.direction[1])
        self.pos = JumpingPfeil.position
    def wert(self):
        if (JumpingPfeil.position[0]<Window.size[0]/2+3 or
            JumpingPfeil.position[0]>Window.size[0]/2+125):
            return -0.4#"Rot"
        elif (JumpingPfeil.position[0]<Window.size[0]/2+38 or
              JumpingPfeil.position[0]>Window.size[0]/2+95):
            return -0.3#"Orange"
        elif (JumpingPfeil.position[0]<Window.size[0]/2+65 or
        	  JumpingPfeil.position[0]>Window.size[0]/2+70):
            return -0.2#"Gelb"
        else:
            return 0.1#"Grün"


class JumpingGuy(Widget):
    position=(Window.size[0]/2,400)
    direction = (0,0)
    speed = 10
    level = 0.4
    flying_since = 0
    bild = StringProperty("Typ.png")
    def move(self):
        self.pos = go(JumpingGuy)
        if JumpingGame.status == "FlyUp":
            self.flying_since = self.flying_since + 1
            if (self.flying_since>=
                (self.level*(1+self.level*2)+JumpingPfeil.wert(JumpingPfeil))*100):
                JumpingGuy.direction =(0,0)
                JumpingGame.status = "Stop"
                global i
                i = -150

class JumpingUniverse(Widget):
    pass
            
class JumpingTrampoline(Widget):
    position = (Window.size[0]/2-100, 0)
    direction = (0,0)
    source = StringProperty("trampolin1.png")
    def move(self):
        self.pos = go(JumpingTrampoline)

class JumpingBuildings(Widget):
    position = (0,0)
    direction = (0,0)
    def move(self):
        self.pos = go(JumpingBuildings)


class JumpingShowlevel(Label):
    position =(JumpingGame.size)
    color = (1,1,1,1)
    atext = StringProperty("Level: " + str(int(JumpingGuy.level*10)-3))
    def set_text(self):
        self.atext = "Level: " + str(int(JumpingGuy.level*10)-3)

class JumpingShowlevelbackground(Widget):
    size = (75,30)
    

from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')
Config.write()
if __name__ == "__main__":
    Builder.load_file('Jumping.kv')###
    JumpingApp().run()
