import json

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from QuizGame import QuizGame


class StartScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.load_scores()

        self.layout = GridLayout(cols=2, rows=6, size_hint=(1, 0.7))
        self.intro_label = Label(text="Welcome to the Quiz Game!", font_size='24sp', color=(0, 0, 1, 1), pos_hint={'x': 0, 'y': 0.3})
        self.materiaalkunde_button = Button(text="Materiaalkunde", on_press=self.start_game_materiaalkunde, background_color=(0, 0, 1, 1), size_hint=(4, 1))
        self.materiaalkundeTotalLabel = Label(text=self.total_score_materiaalkunde, color=(0, 0, 1, 1))
        self.mmvc_button = Button(text="Mechanica van materialen, vloeistoffen en constructies", on_press=self.start_game_mmvc, background_color=(0, 0, 1, 1), size_hint=(4, 1))
        self.mmvcTotalLabel = Label(text=self.total_score_mmvc, color=(0, 0, 1, 1))
        self.bvc_button = Button(text="Basistechnieken voor computersimulaties", on_press=self.start_game_bvc, background_color=(0, 0, 1, 1), size_hint=(4, 1))
        self.bvcTotalLabel = Label(text=self.total_score_bvc, color=(0, 0, 1, 1))
        self.stat_button = Button(text="toegepaste statistiek", on_press=self.start_game_stat, background_color=(0, 0, 1, 1), size_hint=(4, 1))
        self.statTotalLabel = Label(text=self.total_score_stat, color=(0, 0, 1, 1))
        self.vub_quiz = Button(text="VUB", on_press=self.start_game_vub, background_color=(0, 0, 1, 1), size_hint=(4, 1))
        self.vubTotalLabel = Label(text=self.total_score_vub, color=(0, 0, 1, 1))

        self.add_widget(self.intro_label)
        self.layout.add_widget(self.materiaalkunde_button)
        self.layout.add_widget(self.materiaalkundeTotalLabel)
        self.layout.add_widget(self.mmvc_button)
        self.layout.add_widget(self.mmvcTotalLabel)
        self.layout.add_widget(self.bvc_button)
        self.layout.add_widget(self.bvcTotalLabel)
        self.layout.add_widget(self.stat_button)
        self.layout.add_widget(self.statTotalLabel)
        self.layout.add_widget(self.vub_quiz)
        self.layout.add_widget(self.vubTotalLabel)
        self.add_widget(self.layout)

    def start_game_bvc(self, instance):
        bvc_quiz = QuizGame(question_type="bvc", name="quiz_bvc")
        self.clear_widgets()
        self.add_widget(bvc_quiz)

    def start_game_mmvc(self, instance):
        mmvc_quiz = QuizGame(question_type="mmvc", name="quiz_mmvc")
        self.clear_widgets()
        self.add_widget(mmvc_quiz)

    def start_game_materiaalkunde(self, instance):
        materiaalkunde_quiz = QuizGame(question_type="Materiaalkunde", name="materiaalkunde_quiz")
        self.clear_widgets()
        self.add_widget(materiaalkunde_quiz)

    def start_game_stat(self, instance):
        stat_quiz = QuizGame(question_type="stat", name="stat_quiz")
        self.clear_widgets()
        self.add_widget(stat_quiz)

    def start_game_vub(self, instance):
        vub_quiz = QuizGame(question_type="VUB", name="vub_quiz")
        self.clear_widgets()
        self.add_widget(vub_quiz)

    def load_scores(self):
        try:
            with open('scores.json', 'r') as file:
                data = json.load(file)
                self.total_score_materiaalkunde = str(data.get('total_score_materiaalkunde', 0))
                self.total_score_mmvc = str(data.get('total_score_mmvc', 0))
                self.total_score_bvc = str(data.get('total_score_bvc', 0))
                self.total_score_stat = str(data.get('total_score_stat', 0))
                self.total_score_vub = str(data.get('total_score_vub', 0))
        except FileNotFoundError:
            self.total_score_materiaalkunde = "0"
            self.total_score_mmvc = "0"
            self.total_score_bvc = "0"
            self.total_score_stat = "0"
            self.total_score_vub = "0"

    def start_game(self, instance):
        self.manager.current = 'quiz'