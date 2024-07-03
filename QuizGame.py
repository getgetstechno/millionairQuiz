import json
import random

import kivy
import serial
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen


class QuizGame(Screen):

    SCORES = [0, 100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 125000, 250000, 500000, 1000000]
    SCORES_setPoint = [0, 15, 34, 44, 58, 76, 94, 112, 130, 145, 165, 184, 201, 219, 237, 255]

    def __init__(self, question_type, **kwargs):
        super().__init__(**kwargs)
        self.question_type = question_type # is dat weg of niet???
        self.load_scores()
        self.question = None
        self.scoreLabel = None
        self.question_label = None
        self.option_buttons = None
        self.layout = None
        self.quiz_layout = None
        self.score_layout = None
        self.scoreLabel = None
        self.score_labels = None
        self.serial_port = None
        self.fifty_fifty_button = None
        self.get_right_answer_button = None
        self.next_question_button = None
        self.fifty_fifty_joker_available = True
        self.get_right_answer_joker_available = True
        self.next_question_joker_available = True
        self.highest_score = 0
        self.total_score = 0
        self.current_question_index = 0
        self.score_index = 0

        if self.question_type == "bvc":
            self.total_score = self.total_score_bvc
        elif self.question_type == "mmvc":
            self.total_score = self.total_score_mmvc
        elif self.question_type == "Materiaalkunde":
            self.total_score = self.total_score_materiaalkunde
        elif self.question_type == "stat":
            self.total_score = self.total_score_stat
        elif self.question_type == "VUB":
            self.total_score = self.total_score_vub

        self.display_question()
        # problem for now is that this method is always called even when we're playing in another categorie
        """oproep functie, display_question en add_joker_buttons"""

    def load_scores(self):
        try:
            with open('scores.json', 'r') as file:
                data = json.load(file)
                self.total_score_materiaalkunde = str(data.get('total_score_materiaalkunde', 0))
                self.total_score_mmvc = str(data.get('total_score_bvc', 0))
                self.total_score_bvc = str(data.get('total_score_bvc', 0))
                self.total_score_stat = str(data.get('total_score_stat', 0))
                self.total_score_vub = str(data.get('total_score_vub', 0))
        except FileNotFoundError:
            self.total_score_materiaalkunde = "0"
            self.total_score_mmvc = "0"
            self.total_score_bvc = "0"
            self.total_score_stat = "0"
            self.total_score_vub = "0"

    def update_scores(self, score):
        total = int(self.total_score)
        print("total before", total)
        total += score
        print("total after", total)
        self.total_score = str(total)

    def save_scores(self):
        with open('scores.json', 'w') as file:
            json.dump({'total_score_bvc': self.total_score_bvc,
                       'total_score_mmvc': self.total_score_mmvc,
                       'total_score_materiaalkunde': self.total_score_materiaalkunde,
                       'total_score_vub': self.total_score_vub,
                       'total_score_stat': self.total_score_stat}, file)

    def display_question(self):
        self.load_scores()
        self.questions = self.load_questions_from_json()    # oproep vragen nemen en bijhouden in lijst
        self.clear_widgets()
        self.question_label = Label(text=self.questions[self.current_question_index]["question"], size_hint=(1, 2), color=(0, 0.2, 0.8, 1), font_size='20sp')
        self.option_buttons = [Button(text=option, font_size="16sp", background_color=(0, 0, 1, 1)) for option in self.questions[self.current_question_index]["options"]]
        self.total_score_label = Label(text="total score : "+self.total_score, color=(0, 0.2, 0.8, 1), font_size='20sp')
        self.layout = BoxLayout(orientation='horizontal')
        self.quiz_layout = BoxLayout(orientation='vertical', size_hint=(3, 1))
        self.quiz_layout.add_widget(self.question_label)
        self.quiz_layout.add_widget(self.total_score_label)
        self.score_layout = BoxLayout(orientation='vertical', size_hint=(1, 1))
        self.scoreLabel = Label(text=str(self.SCORES[self.score_index]), font_size='20sp', pos_hint={'x': 0, 'y': 4}, height=100, color=(0, 0.2, 0.8, 1))
        self.score_layout.add_widget(self.scoreLabel)
        self.score_labels = [Label(text=str(option), font_size="16sp", color=(0, 0.2, 0.8, 1)) for option in sorted(self.SCORES, reverse=True)]

        for button in self.option_buttons:
            button.bind(on_press=self.check_answer_ui)          # roept functie check_anwer_ui
            self.quiz_layout.add_widget(button)

        for labels in self.score_labels:
            if labels.text == "0":
                labels.color = [0, 1, 0, 1]
            self.score_layout.add_widget(labels)

        try:
            self.serial_port = serial.Serial('COM4', 9600)  # Change 'COM1' to your serial port
        except serial.SerialException:
            print("Serial port not found or could not be opened.")

        if self.serial_port:    # if serial_port exist...
            # boolean maken en activeren alleen als volgende vraag aan is
            kivy.clock.Clock.schedule_interval(self.read_serial_data, 0.1)         # lees de data elke 100ms als die bestaat

        self.layout.add_widget(self.quiz_layout)
        self.layout.add_widget(self.score_layout)
        self.add_widget(self.layout)
        self.add_joker_buttons()  # Add joker buttons to the screen
        """roept functie read_serial_data, load_question_from_json, check_answer_ui"""

    def update_score_panel(self):   # wordt opgeroepen vanuit check_answer
        # doorsturen van de score naar de serial port
        self.score_index += 1
        self.scoreLabel.text = str(self.SCORES[self.score_index])
        for labels in self.score_labels:
            # print(labels.text)
            if labels.text == self.scoreLabel.text:
                # knop gevonden die moet groen worden
                labels.color = [0, 1, 0, 1]  # Set the color to green if it matches the current score

    def load_questions_from_json(self):
        filename = f"questions_{self.question_type.lower()}.json"
        with open(filename, "r") as file:
            data = json.load(file)
        return random.sample(data['questions'], len(data['questions']))

    def check_answer_ui(self, instance):
        print(instance.text)
        selected_option = instance.text
        for button in self.option_buttons:
            button.disabled = True
        Clock.schedule_once(lambda dt: self.check_answer(selected_option), 1)

    def check_answer_serial(self, button_index):
        selected_option = self.questions[self.current_question_index]["options"][button_index]
        print(selected_option)
        self.check_answer(selected_option)

    def check_answer(self, selected_option):
        correct_answer = self.questions[self.current_question_index]["correct_answer"]
        if selected_option == correct_answer:
            self.update_score_panel()
            print("Correct!")
            try:
                if self.serial_port:
                    self.serial_port.write(f'S{self.SCORES_setPoint[self.score_index]}\r\n'.encode('utf-8'))
                    print("score : ", self.SCORES_setPoint[self.score_index])
            except serial.SerialException:
                pass
            #Clock.schedule_once(lambda dt: self.show_answer_feedback(True), 1)
            self.show_answer_feedback(True)
        else:
            print("Incorrect!")
            self.show_answer_feedback(False)
            #kivy.clock.Clock.schedule_interval(self.read_serial_data, 0.1)
            #Clock.schedule_once(lambda dt: self.show_answer_feedback(False), 1)

    def show_answer_feedback(self, is_correct):
        for button in self.option_buttons:
            if is_correct == True:
                button.background_color = (0, 1, 0, 1)
            else:
                button.background_color = (1, 0, 0, 1)
        Clock.schedule_once(self.next_question if is_correct else self.end_game, 1)

    def next_question(self, dt):
        for button in self.option_buttons:
            button.background_color = (0, 0, 1, 1)  # Reset to default color
            button.disabled = False

        print(self.current_question_index)
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.question_label.text = self.questions[self.current_question_index]["question"]
            for index, button in enumerate(self.option_buttons):
                button.text = self.questions[self.current_question_index]["options"][index]

    def end_game(self, dt):
        self.update_scores(self.SCORES[self.score_index])
        if self.serial_port:
            self.serial_port.write(f'S{self.SCORES_setPoint[0]}\r\n'.encode('utf-8'))
        self.clear_widgets()
        self.layout.clear_widgets()
        if self.score_index != 0:
            final_score = self.SCORES[self.score_index]  # Get the last score achieved
        else:
            final_score = 0
        end_label = Label(text=f'Game Over! Your final score is: {final_score}', color=(0, 0.2, 0.8, 1))
        self.layout.add_widget(end_label)

        # Add a button to start over again
        restart_button = Button(text="Restart", size_hint=(1, 0.5), pos_hint={'x':0.5, 'y':0.25}, background_color=(0, 0, 1, 1))
        restart_button.bind(on_press=self.restart_game)
        self.layout.add_widget(restart_button)
        self.add_widget(self.layout)

        if self.question_type == "bvc":
            self.total_score_bvc = self.total_score
        elif self.question_type == "mmvc":
            self.total_score_mmvc = self.total_score
        elif self.question_type == "Materiaalkunde":
            self.total_score_materiaalkunde = self.total_score
        elif self.question_type == "stat":
            self.total_score_stat = self.total_score
        elif self.question_type == "VUB":
            self.total_score_vub = self.total_score
        self.save_scores()

    def restart_game(self, instance):
        # Reset game state
        self.fifty_fifty_joker_available = True
        self.get_right_answer_joker_available = True
        self.next_question_joker_available = True
        self.time_left = 31
        self.clear_widgets()
        self.current_question_index = 0
        self.score_index = 0
        self.display_question()

    def read_serial_data(self, dt):
        try:
            if self.serial_port and self.serial_port.in_waiting > 0:
                button_index = int(self.serial_port.read().decode()) - 1  # Decrement by 1 to convert to 0-based index
                # probleem is dat die deze waarde altijd aan het oproepen is...
                self.check_answer_serial(button_index)
        except serial.SerialException:
            print("Error reading from serial port.")

    def fifty_fifty_joker(self):
        # Use the 50/50 joker
        if self.fifty_fifty_joker_available == True:
            question_data = self.questions[self.current_question_index]
            options = question_data['options']
            correct_answer = question_data['correct_answer']
            wrong_answers = [option for option in options if option != correct_answer]
            wrong_answers.pop(random.randrange(len(wrong_answers)))
            for button in self.option_buttons:
                if button.text in wrong_answers:
                    button.disabled = True
            self.fifty_fifty_button.disabled = True
            self.fifty_fifty_joker_available = False

    def get_right_answer_joker(self):
        if self.get_right_answer_joker_available == True:
            # Use the get right answer joker
            correct_answer = self.questions[self.current_question_index]['correct_answer']
            # Show the correct answer to the player
            modal_view = ModalView(size_hint=(None, None), size=(400, 200))
            modal_view.add_widget(Label(text=f"The correct answer is: {correct_answer}", font_size=20))
            modal_view.open()
            self.get_right_answer_button.disabled = True
            self.get_right_answer_joker_available = False

    def next_question_joker(self):
        # Use the next question joker
        if self.next_question_joker_available == True:
            self.next_question(None)
            self.next_question_button.disabled = True
            self.next_question_joker_available = False

    def add_joker_buttons(self):
        # Add joker buttons to the screen
        self.fifty_fifty_button = Button(text="50/50 Joker", size_hint=(None, None), size=(350, 100), pos_hint={'x':0.05, 'y':0.9}, background_color=(0, 0, 1, 1))
        self.fifty_fifty_button.bind(on_press=lambda instance: self.fifty_fifty_joker())

        self.get_right_answer_button = Button(text="Get Right Answer Joker", size_hint=(None, None), size=(350, 100), pos_hint={'x':0.3, 'y':0.9}, background_color=(0, 0, 1, 1))
        self.get_right_answer_button.bind(on_press=lambda instance: self.get_right_answer_joker())

        self.next_question_button = Button(text="Next Question Joker", size_hint=(None, None), size=(350, 100), pos_hint={'x':0.55, 'y':0.9}, background_color=(0, 0, 1, 1))
        self.next_question_button.bind(on_press=lambda instance: self.next_question_joker())

        self.add_widget(self.fifty_fifty_button)
        self.add_widget(self.get_right_answer_button)
        self.add_widget(self.next_question_button)