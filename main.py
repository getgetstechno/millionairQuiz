from kivy.app import App
from kivy.core.window import Window

from kivy.uix.screenmanager import ScreenManager, SlideTransition
from QuizGame import QuizGame
from StartScreen import StartScreen

'''
TO DO list:
- probleem bij miljoen aanpassen
- meerdere categorieen --> opgelost
- jokers toevoegen --> 
- kernwoorden vragen en dan aan chatgpt vragen om vragen te genereren en die dan gebruiken... of zelf een aantal categorieen maken
- color when button click --> oplgelost
- timer toevoegen --> opgelost --> maar terug eruit gehaald want is misserie en niet echt nodig
- hartslag meer --> tijd minder
- facial recognition --> 
- veel bugs oplossen

update 5/3/2025
--> toevoegen van extra scherm om te bepalen wat we willen aanduiden op die toren
--> koppelen van de score met de toren (1)
--> vragen veranderen en chatgpt toevoegen
--> volgorde antwoorden aanpassen (in json file of echt in code) 
--> UI aanpassen en kleuren beter maken
--> visual recognition toevoegen 
--> koppelen met die hartsensor

--> timers toevoegen voor buttons zodat die niet 1000x worden opgeroepen als we die gewoon 1 seconde volhouden
--> scoren niet geupdated bij andere quiz --> enkel gevan bij sport --> iets speciaal met sport!!!
'''

class MillionaireGame(App):

    def build(self):
        Window.clearcolor = (0.9, 0.9, 0.9, 1)
        sm = ScreenManager(transition=SlideTransition(direction="left"))
        sm.add_widget(StartScreen(name="start"))
        return sm

if __name__ == "__main__":
    MillionaireGame().run()
