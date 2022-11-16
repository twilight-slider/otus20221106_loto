from __future__ import annotations
from typing import List
import enum
from random import randint
from classes.game_params import Param, GameParams
import os


class Barrel:
    _number: int

    def __init__(self, num: int):
        self.number = num

    def __str__(self):
        return f'(Barrel-{self.number})'

    @property
    def number(self) -> int:
        return self._number

    @number.setter
    def number(self, number: int):
        if type(number) != int:
            raise 'Бочка может быть только с целым значением'
        if number < 0 or number > 90:
            raise f'Бочка может быть только с целым значением от 1 до {GameParams.BARREL_POOL_SIZE}'
        self._number = number


class BarrelPool:
    def __init__(self):
        self._pool = []
        self._extracted_barrels = []
        for i in range(1, GameParams.BARREL_POOL_SIZE + 1):
            self._pool.append(i)

    @property
    def barrels_left(self):
        return len(self._pool)

    @property
    def pool(self):
        return self._pool

    @property
    def extracted_barrels(self):
        return self._extracted_barrels

    def extract_num(self) -> int:
        pool_size = len(self._pool)
        if pool_size == 0:
            print('Pool is empty')
            return 0
        i = randint(0, len(self._pool) - 1)
        num = self._pool[i]
        self._extracted_barrels.append(num)
        self._pool.remove(num)
        return num

    def get_barrel(self) -> Barrel:
        num = self.extract_num()
        return Barrel(num)


class CardRow:
    def __init__(self, barrel_pool: BarrelPool):
        self.columns = [0] * GameParams.CARD_COLUMNS
        filled_columns = []
        numbers = []
        for i in range(0, GameParams.CARD_COLUMNS):
            filled_columns.append(i)
            if i < GameParams.CARD_ROW_NUMBERS:
                numbers.append(barrel_pool.extract_num())
        numbers.sort()

        for i in range(0, GameParams.CARD_ROW_NUMBERS):
            filled_column_index = randint(0, len(filled_columns) - 1)
            fc = filled_columns[filled_column_index]
            self.columns[fc] = -1
            filled_columns.remove(filled_columns[filled_column_index])

        columns_i = 0
        self.left_columns = []
        for i in range(0, GameParams.CARD_COLUMNS):
            if self.columns[i] == -1:
                self.columns[i] = numbers[columns_i]
                columns_i += 1
        self._numbers_left = GameParams.CARD_ROW_NUMBERS

    def __str__(self):
        string = ''
        for i in range(0, len(self.columns)):
            col_str = (
                str(self.columns[i]) if self.columns[i] > 0
                else " " if self.columns[i] == 0
                else f"*{abs(self.columns[i])}"
            )
            string = string + (' ' * len(str(GameParams.BARREL_POOL_SIZE)) + col_str)[-GameParams.COL_WIDTH:]
        return string

    def get_number_pos(self, number: int) -> int:
        try:
            return self.columns.index(number)
        except ValueError:
            return -1

    def mark_column_barreled(self, column_i: int) -> bool:
        if column_i > -1:
            self.columns[column_i] = -1 * self.columns[column_i]
            self._numbers_left = self._numbers_left - 1
            return True
        return False

    @property
    def numbers_left(self):
        return self._numbers_left


class Card:
    def __init__(self):
        barrel_pool = BarrelPool()
        self.card_rows = []
        self._numbers_left = 0
        for i in range(0, GameParams.CARD_ROWS):
            card_row = CardRow(barrel_pool)
            self.card_rows.append(card_row)
            self._numbers_left = self._numbers_left + card_row.numbers_left

    @property
    def numbers_left(self):
        return self._numbers_left

    def __str__(self):
        horiz_line = '-' * GameParams.CARD_COLUMNS * GameParams.COL_WIDTH
        string = horiz_line
        for i in range(0, len(self.card_rows)):
            string = string + '\n\r' + str(self.card_rows[i])
        string = string + '\n\r' + horiz_line
        return string

    def get_number_pos(self, number: int) -> (int, int):
        for i in range(0, GameParams.CARD_ROWS):
            _row_number_pos = self.card_rows[i].get_number_pos(number)
            if _row_number_pos > -1:
                return i, _row_number_pos
        return -1, -1

    def mark_pos_barreled(self, position: (int, int)) -> bool:
        if position[0] < 0:
            return False
        _pos_barreled = self.card_rows[position[0]].mark_column_barreled(position[1])
        if _pos_barreled:
            self._numbers_left = self._numbers_left - 1
        return _pos_barreled


class PlayerType(enum.Enum):
    Computer = 0
    Human = 1


class Player:
    player_type: PlayerType
    name: str
    is_active: bool
    card: Card

    def __init__(self, player_type: PlayerType, number: int):
        self.is_active = True
        self.player_type = player_type
        if player_type == PlayerType.Computer:
            self.name = f'Компьютер №{number}'
        else:
            self.name = self._get_human_name(number).value
        self.card = Card()

    @staticmethod
    def _get_human_name(number) -> Param:
        message = f'Введите имя игрока-человека №{number}? (строка длиной [1..20] символов)'
        _player_human_name = Param(
            name=f'human_{number}_name',
            label=f'Имя игрока-человека №{number}',
            value=f'Игрок-человек №{number}',
            question={
                'type': 'input',
                'name': 'answer',
                'message': message,
            },
            answer_type=str,
            correct=lambda x: 1 <= len(x) <= 20
        )
        _player_human_name.input()
        return _player_human_name

    def check_number(self, barrel: Barrel):
        card_number_pos = self.card.get_number_pos(barrel.number)
        print('*' * 30)
        print(f'{self.name}: {barrel}')
        print(self.card)

        message = f'{self.name} закончил свой ход.'  # default message

        if self.player_type == PlayerType.Computer:
            if card_number_pos != (-1, -1):
                self.card.mark_pos_barreled(card_number_pos)
                message = f'{self.name} вычеркивает номер {barrel.number}!'
                if self.card.numbers_left == 0:
                    message = message + f'\n\rУ {self.name} закончилась карточка!'

        else:  # PlayerType.Human
            check_number = GameParams.prompt_player_number_deletion(self.name, barrel.number)
            if check_number:
                marked_successfully = self.card.mark_pos_barreled(card_number_pos)
                if not marked_successfully:
                    message = 'Ошибочка вышла, такого номера нет.'
                    self.is_active = False
                else:
                    message = f'{self.name} вычеркивает номер {barrel.number}!'

            elif card_number_pos != (-1, -1):
                message = 'Ошибочка вышла, есть такой номер. Надо было вычеркивать.'
                self.is_active = False

        print(message)


class GameResult(enum.Enum):
    Continue = 0
    Win = 1
    Draw = 2


class Game:
    players: List[Player]
    barrel_pool: BarrelPool

    def __init__(self, game_params: GameParams):
        self.game_params = game_params

    def create_players(self):
        self.players = []

        for i in range(1, self.game_params.players_count_total.value - self.game_params.players_count_human.value + 1):
            x = Player(PlayerType.Computer, i)
            self.players.append(x)

        for i in range(1, self.game_params.players_count_human.value + 1):
            x = Player(PlayerType.Human, i)
            self.players.append(x)

    @property
    def active_players_count(self) -> int:
        k = 0
        for player in self.players:
            if player.is_active:
                k += 1
        return k

    def turn(self):
        os.system('cls')
        barrel = self.barrel_pool.get_barrel()
        print(f'{barrel}, осталось: {self.barrel_pool.barrels_left}')
        for player in self.players:
            if not player.is_active:
                print(f'{player.name} не играет.')
            else:
                player.check_number(barrel)

    @property
    def game_result(self) -> GameResult:
        _game_result = GameResult.Continue
        message = 'Продолжаем...'
        if self.active_players_count == 0:
            _game_result = GameResult.Draw
            message = 'Все проиграли xD'
        elif self.active_players_count == 1:
            _game_result = GameResult.Win
            for p in self.players:
                if p.is_active:
                    message = f'Победитель: {p.name}!'
                    break
        else:
            winners = []
            for player in self.players:
                if player.card.numbers_left == 0:
                    winners.append(player)

            if len(winners) == 1:
                message = f'Победитель: {winners[0].name}!'
                _game_result = GameResult.Win
            elif len(winners) == len(self.players):
                message = f'У всех игроков закрыты карточки! Ничья!'
                _game_result = GameResult.Draw
            elif len(winners) > 1:
                message = 'Победители:'
                for player in winners:
                    message = message + f'\n\r{player.name}'
                _game_result = GameResult.Win

        _active_human = 0
        for player in self.players:
            if player.is_active and player.player_type == PlayerType.Human:
                _active_human += 1

        if _active_human > 0 or _game_result != GameResult.Continue:
            input(f'{message}\n\r\n\r(нажмите Enter...)')
        os.system('cls')
        return _game_result

    def play(self):
        self.create_players()
        self.barrel_pool = BarrelPool()
        while self.game_result == GameResult.Continue:
            self.turn()
        input('Конец игры\n\r\n\r(нажмите Enter)')
