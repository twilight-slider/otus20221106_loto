from classes.game_params import GameParams
from classes.lotto import Game


def main():
    game = Game(GameParams())
    while not game.game_params.menu() == 'exit':
        game.play()


if __name__ == '__main__':
    main()
