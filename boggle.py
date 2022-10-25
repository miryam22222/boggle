import board as Board
import time

GAME_LOOP_TIME = 50
ROUND_TIME_MINUTES = 180


def words(filename):
    """This function returns a set containing all words in the given file"""
    words = set()
    with open(filename) as data:
        for word in data:
            words.add(word.strip())
        return words


class Game:
    """This class runs a game of boggle"""

    FILE_NAME = "boggle_dict.txt"

    def __init__(self):
        self.board = Board.Board()
        self.score = 0
        self.found_words = []
        self.timer = time.time()
        self.words = words(self.FILE_NAME)
        self.timer = ROUND_TIME_MINUTES * 1000
        self.score = 0
        self.msg_to_print = ""

    def run(self):
        """Runs a game"""
        self.do_loop()
        self.board.root.mainloop()

    def do_loop(self):
        """Runs the game every GAME_LOOP_TIME milliseconds"""
        self.game_loop()
        self.board.root.update()
        self.board.root.after(GAME_LOOP_TIME, self.do_loop)

    def check_word(self):
        """Checks if the guessed word is in the optional words"""
        if self.board.get_is_not_pressed():
            word_to_check = self.board.get_saved_word().upper()
            if word_to_check in self.words:
                if word_to_check not in self.found_words:
                    self.found_words.append(word_to_check)
                    self.board.add_found_word(word_to_check)
                    self.score += len(word_to_check) ** 2
                    self.board.set_score(self.score)
            #         self.board.msg_to_print_label.config(text=word_to_check, bg="green")
            #     else:
            #         self.board.msg_to_print_label.config(text="Word already found", bg="yellow")
            # else:
            #     self.board.msg_to_print_label.config(text="LOSER!", bg="red")

    def game_loop(self):
        """Runs a single round"""
        if self.board.get_running():
            self.board.run_board()
            if self.timer == 0:
                self.board.end(False)
            self.check_word()
            if not self.board.get_is_exit_pressed():
                self.set_time()
            self.board.timer(self.timer // 60000,
                             int((self.timer / 1000) % 60))
        else:
            self.score = 0
            self.board.set_score(self.score)
            self.timer = ROUND_TIME_MINUTES * 1000
            self.board.timer(self.timer // 60000,
                             int((self.timer / 1000) % 60))

    def set_time(self):
        self.timer -= GAME_LOOP_TIME


if __name__ == '__main__':
    game = Game()
    game.run()
