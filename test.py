hfhyfj,jug,u
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QRadioButton, QButtonGroup, 
                             QPushButton, QStackedWidget, QProgressBar)
from PyQt5.QtCore import Qt
class PsychotypeTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.answers = []
        
    def initUI(self):
        self.setWindowTitle('Тест на психотип - Карнаух Иван')
        self.setGeometry(300, 200, 600, 400)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        # Создаем stacked widget для переключения между вопросами
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)
        
        # Прогресс бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(4)
        self.layout.insertWidget(0, self.progress_bar)
        
        # Создаем страницы с вопросами
        self.create_question_pages()
        
        # Кнопки навигации
        self.nav_layout = QHBoxLayout()
        self.prev_button = QPushButton('Назад')
        self.next_button = QPushButton('Далее')
        self.result_button = QPushButton('Получить результат')
        self.result_button.hide()
        
        self.prev_button.clicked.connect(self.previous_question)
        self.next_button.clicked.connect(self.next_question)
        self.result_button.clicked.connect(self.show_result)
        
        self.nav_layout.addWidget(self.prev_button)
        self.nav_layout.addWidget(self.next_button)
        self.nav_layout.addWidget(self.result_button)
        self.layout.addLayout(self.nav_layout)
        
        self.update_navigation()
        
    def create_question_pages(self):
        self.questions = [
            {
                'question': '1. Как вы обычно реагируете на стрессовые ситуации?',
                'options': [
                    'А) Стараюсь сохранять спокойствие и искать рациональное решение',
                    'Б) Эмоционально реагирую, могу вспылить или расстроиться',
                    'В) Избегаю конфликта, стараюсь уйти от ситуации',
                    'Г) Ищу поддержки у окружающих, делюсь переживаниями'
                ]
            },
            {
                'question': '2. Как вы предпочитаете проводить свободное время?',
                'options': [
                    'А) В одиночестве, занимаясь хобби или саморазвитием',
                    'Б) В активной компании, на мероприятиях или вечеринках',
                    'В) В спокойной обстановке с близкими людьми',
                    'Г) Планируя и организуя что-то новое'
                ]
            },
            {
                'question': '3. Как вы принимаете важные решения?',
                'options': [
                    'А) Тщательно анализирую все "за" и "против"',
                    'Б) Руководствуюсь интуицией и чувствами',
                    'В) Советуюсь с другими людьми',
                    'Г) Действую импульсивно, по ситуации'
                ]
            },
            {
                'question': '4. Как вы ведете себя в новом коллективе?',
                'options': [
                    'А) Наблюдаю со стороны, сначала изучаю людей',
                    'Б) Быстро нахожу общий язык со всеми',
                    'В) Присоединяюсь к небольшой группе "своих"',
                    'Г) Стараюсь занять лидирующую позицию'
                ]
            }
        ]
        
        self.radio_groups = []
        
        for i, question_data in enumerate(self.questions):
            page = QWidget()
            layout = QVBoxLayout(page)
            
            # Вопрос
            question_label = QLabel(question_data['question'])
            question_label.setStyleSheet('font-size: 14pt; font-weight: bold; margin: 20px;')
            question_label.setWordWrap(True)
            layout.addWidget(question_label)
            
            # Группа радиокнопок
            button_group = QButtonGroup(page)
            button_group.setExclusive(True)
            
            for j, option in enumerate(question_data['options']):
                radio = QRadioButton(option)
                radio.setStyleSheet('font-size: 12pt; margin: 10px;')
                radio.option_index = j  # Сохраняем индекс варианта
                button_group.addButton(radio)
                layout.addWidget(radio)
            
            self.radio_groups.append(button_group)
            layout.addStretch()
            self.stacked_widget.addWidget(page)
    
    def update_navigation(self):
        current_index = self.stacked_widget.currentIndex()
        self.prev_button.setVisible(current_index > 0)
        
        if current_index == len(self.questions) - 1:
            self.next_button.hide()
            self.result_button.show()
        else:
            self.next_button.show()
            self.result_button.hide()
            
        self.progress_bar.setValue(current_index + 1)
    
    def next_question(self):
        current_index = self.stacked_widget.currentIndex()
        button_group = self.radio_groups[current_index]
        
        # Проверяем, выбран ли ответ
        if button_group.checkedButton():
            # Сохраняем ответ (A=0, B=1, C=2, D=3)
            self.answers.append(button_group.checkedButton().option_index)
            
            if current_index < len(self.questions) - 1:
                self.stacked_widget.setCurrentIndex(current_index + 1)
                self.update_navigation()
        else:
            # Можно добавить сообщение об ошибке
            pass
    
    def previous_question(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index > 0:
            # Удаляем последний ответ при возврате
            if len(self.answers) > current_index - 1:
                self.answers = self.answers[:current_index-1]
            self.stacked_widget.setCurrentIndex(current_index - 1)
            self.update_navigation()
    
    def show_result(self):
        # Сохраняем ответ на последний вопрос
        current_index = self.stacked_widget.currentIndex()
        button_group = self.radio_groups[current_index]
        
        if button_group.checkedButton():
            self.answers.append(button_group.checkedButton().option_index)
            
            # Анализируем результаты
            result = self.analyze_results()
            
            # Создаем страницу с результатом
            result_page = QWidget()
            layout = QVBoxLayout(result_page)
            
            result_label = QLabel('Ваш результат:')
            result_label.setStyleSheet('font-size: 16pt; font-weight: bold; margin: 20px;')
            layout.addWidget(result_label)
            
            description_label = QLabel(result)
            description_label.setStyleSheet('font-size: 12pt; margin: 20px;')
            description_label.setWordWrap(True)
            layout.addWidget(description_label)
            
            restart_button = QPushButton('Пройти тест заново')
            restart_button.clicked.connect(self.restart_test)
            layout.addWidget(restart_button)
            
            self.stacked_widget.addWidget(result_page)
            self.stacked_widget.setCurrentWidget(result_page)
            
            # Скрываем кнопки навигации
            self.prev_button.hide()
            self.next_button.hide()
            self.result_button.hide()
            self.progress_bar.hide()
    
    def analyze_results(self):
        # Простой анализ на основе преобладающих ответов
        answer_counts = [0, 0, 0, 0]  # A, B, C, D
        
        for answer in self.answers:
            answer_counts[answer] += 1
        
        max_count = max(answer_counts)
        predominant_answers = [i for i, count in enumerate(answer_counts) if count == max_count]
        
        # Описания психотипов
        psychotypes = {
            0: "РАЦИОНАЛ\n\nВы логичны, последовательны и практичны. "
               "Принимаете решения на основе анализа фактов, а не эмоций. "
               "Цените структуру и порядок в жизни.",
               
            1: "ЭМОТИВ\n\nВы чувствительны, эмоциональны и восприимчивы. "
               "Руководствуетесь сердцем, а не разумом. Обладаете развитой эмпатией "
               "и хорошо понимаете чувства других людей.",
               
            2: "ИНТРОВЕРТ\n\nВы сосредоточены на своем внутреннем мире. "
               "Цените глубокие отношения с небольшим кругом близких людей. "
               "Нуждаетесь в личном пространстве и времени для восстановления сил.",
               
            3: "ЛИДЕР\n\nВы активны, инициативны и уверены в себе. "
               "Легко берете на себя ответственность и организуете других людей. "
               "Стремитесь к достижению целей и новым вызовам."
        }
        
        if len(predominant_answers) == 1:
            return psychotypes[predominant_answers[0]]
        else:
            # Смешанный тип
            mixed_types = " + ".join([["Рационал", "Эмотив", "Интроверт", "Лидер"][i] for i in predominant_answers])
            return f"СМЕШАННЫЙ ТИП: {mixed_types}\n\nВы обладаете чертами нескольких психотипов, " \
                   "что делает вас гибким и многогранным человеком, способным адаптироваться " \
                   "к разным ситуациям и людям."
    
    def restart_test(self):
        # Сбрасываем тест
        self.answers = []
        for group in self.radio_groups:
            group.setExclusive(False)
            for button in group.buttons():
                button.setChecked(False)
            group.setExclusive(True)
        
        self.stacked_widget.setCurrentIndex(0)
        self.update_navigation()
        self.progress_bar.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PsychotypeTest()
    window.show()
    sys.exit(app.exec_())
