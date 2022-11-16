# -*- coding: utf-8 -*-
# PyInquirer -- примеры: https://github.com/CITGuru/PyInquirer/tree/master/examples
import os
from PyInquirer import prompt


class Param:
    def __init__(self, name, label, value, question, answer_type: type,
                 correct: callable = None, map_answer: callable = None):
        self.name = name
        self.label = label
        self.value = value
        self.question = question
        self.answer_type = answer_type
        self.correct = correct
        self.map_answer = map_answer

    def input(self):
        _answer_typed = None
        _is_correct = (self.correct is None)

        while not _is_correct:
            answer = prompt(self.question)['answer']
            try:
                _answer_typed = self.answer_type(str(answer).strip())
                if self.correct(_answer_typed):
                    _is_correct = True
            except ValueError:
                print('Введен некорректный ответ. Попробуем еще раз:')

        if self.map_answer is not None:
            self.value = self.map_answer(_answer_typed)
        else:
            self.value = _answer_typed

    def __str__(self):
        return f'{self.label}: {self.value}'


class GameParams:
    MIN_PLAYERS = 2
    MAX_PLAYERS = 4
    MIN_HUMAN_PLAYERS = 1
    MAX_HUMAN_PLAYERS = 2
    BARREL_POOL_SIZE = 6  # 90
    CARD_ROWS = 1  # 3
    CARD_COLUMNS = 10  # 9
    CARD_ROW_NUMBERS = 5  # 5
    # ===========
    COL_WIDTH = len(str(BARREL_POOL_SIZE)) + 1

    def __init__(self):
        _total_players_str = f"{self.MIN_PLAYERS}" if self.MIN_PLAYERS == self.MAX_PLAYERS \
            else f"{self.MIN_PLAYERS}..{self.MAX_PLAYERS}"
        message = f'Всего игроков? (целое число [{_total_players_str}])'

        self.players_count_total = Param(
            name='_players_count_total',
            label='Всего игроков',
            value=2,
            question={
                'type': 'input',
                'name': 'answer',
                'message': message,
            },
            answer_type=int,
            correct=lambda x: self.MIN_PLAYERS <= x <= self.MAX_PLAYERS
        )

        humans_players_str = f"{self.MIN_HUMAN_PLAYERS}" if self.MIN_HUMAN_PLAYERS == self.MAX_HUMAN_PLAYERS \
            else f"{self.MIN_HUMAN_PLAYERS}..{self.MAX_HUMAN_PLAYERS}"
        message = f'Сколько игроков людей? (целое число [{humans_players_str}])'

        self.players_count_human = Param(
            name='_players_count_human',
            label='Количество игроков-людей',
            value=1,
            question={
                'type': 'input',
                'name': 'answer',
                'message': message,
            },
            answer_type=int,
            correct=lambda x: self.MIN_HUMAN_PLAYERS <= x <= self.MAX_HUMAN_PLAYERS
        )

    # основной метод предоставления параметров
    @property
    def params(self):
        return {
            self.players_count_total.name: self.players_count_total.value,
            self.players_count_human.name: self.players_count_human.value,
        }

    @classmethod
    def prompt_player_number_deletion(cls, player_name: str, number_to_delete: int) -> bool:
        cross_out_str = 'Вычеркиваем.'
        question = {
            'type': 'list',
            'message': f'{player_name}, вычеркиваем [{number_to_delete}]?',
            'name': 'answer',
            'choices': [cross_out_str, 'У меня нет такого номера.']
        }
        answer = prompt(question)['answer']
        return answer == cross_out_str

    def menu(self):
        message = f'*** Лото ***\n\r\n\r',
        _menu_item_play = 'Играть'
        _menu_item_exit = 'Выход'
        answer = 'play'
        while answer not in (_menu_item_play, _menu_item_exit):
            os.system('cls')
            _menu_item_players_count_total = f'Изменить ({self.players_count_total})'
            _menu_item_players_count_human = f'Изменить ({self.players_count_human})'
            question = {
                'type': 'list',
                'message': message,
                'name': 'answer',
                'choices': [
                    _menu_item_play,
                    _menu_item_players_count_total,
                    _menu_item_players_count_human,
                    _menu_item_exit
                ]
            }
            answer = prompt(question)['answer']
            if answer == _menu_item_exit:
                return 'exit'
            if answer == _menu_item_play:
                return 'play'
            elif answer == _menu_item_players_count_total:
                self.players_count_total.input()
            elif answer == _menu_item_players_count_human:
                self.players_count_human.input()
