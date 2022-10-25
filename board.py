import tkinter as tk
from tkinter import messagebox
import boggle_board_randomizer

PHOTO_FILE = "bg_new.png"
INSTRUCTIONS_FILE = "instructions.txt"


def read_instructions(filename):
    """Gets an instructions file, reads it and converts to a string"""
    string = ""
    with open(filename) as data:
        for line in data:
            string = string+line
    return string


class Buttons:
    """The class of all buttons - contains the information about every button
    it gets from the board"""
    def __init__(self, letters_frame, text, row, col):
        self.button = tk.Button(letters_frame, text=text, font=("Courier", 30),
                                bg='pale goldenrod', borderwidth=15,
                                cursor='mouse')
        self.text = text
        self.row = row
        self.col = col

    def get_button(self):
        """Returns the 'id' of a button"""
        return self.button

    def get_text(self):
        """Returns what's written on the button (the letter itself)"""
        return self.text

    def get_row(self):
        """Returns the row in which the button is"""
        return self.row

    def get_col(self):
        """Returns the column in which the button is"""
        return self.col


class Board:
    """The class is responsible for everything that happens on the board"""
    def __init__(self):
        self.board = boggle_board_randomizer.randomize_board()
        self.current_word = ""
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=700, height=700, bg='black')
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.letters_frame = tk.Frame(self.canvas, bg='plum3')
        self.background_image = tk.PhotoImage(file=PHOTO_FILE)
        self.background_label = tk.Label(self.canvas, image=self.background_image)
        # self.msg_to_print_label = tk.Label(self.canvas, text="Have fun ^^")
        self.buttons_list = []
        self.Pressed_Buttons = []
        self.is_not_pressed = False
        self.saved_word = ""
        self.time_frame = tk.LabelFrame(self.canvas)
        self.time_label = tk.Label(self.time_frame)
        self.start_button = tk.Button(self.canvas)
        self.boggle_title = tk.Label(self.canvas)
        self.running = False
        self.score_frame = tk.LabelFrame(self.canvas)
        self.score_label = tk.Label(self.score_frame)
        self.found_words_frame = tk.Frame(self.canvas)
        self.found_words_list = tk.Listbox(self.found_words_frame)
        self.scroll_bar = tk.Scrollbar(self.found_words_frame)
        self.exit_button = tk.Button(self.canvas, command=self.quit_game,
                text='Exit', bg="brown3", fg="seashell2", font=("Times New "
                "Roman", 12, "bold"))
        self.is_exit_pressed = False
        self.instructions_button = tk.Button(self.canvas, text="How Do I "
                "Play??", command=self.show_instructions, font=("Times New "
                "Roman", 14, "bold"), fg="MistyRose2", bg='maroon', height=1,
                width=14, borderwidth=10)
        self.starting_board_graphics()

    def get_is_exit_pressed(self):
        """Returns information about the exit button"""
        return self.is_exit_pressed

    def show_instructions(self):
        """The command function of the instructions button, prints them
        to the screen as a massegebox"""
        MsgBox = tk.messagebox.showinfo("Instructions: ",read_instructions(INSTRUCTIONS_FILE))

    def quit_game(self):
        """The command function of the exit button, hides all frames (except
        the time), asks the player if he's sure he wants to exit the game, if
        yes - turns the game off, else - prints all the buttons and the rast
        information back to the screen"""
        self.is_exit_pressed = True
        self.start_button.pack_forget()
        self.instructions_button.place_forget()
        # self.msg_to_print_label.place_forget()
        if self.running:
            self.letters_frame.place_forget()
            self.found_words_frame.place_forget()
            self.score_frame.place_forget()
        MsgBox = tk.messagebox.askquestion("EXIT", "Are you sure?")
        if MsgBox == "yes":
            exit()
        else:
            tk.messagebox.showinfo("Great!","Lets keep boggling")
            self.start_button.pack()
            self.instructions_button.place(relx=0.375, rely=0.3)
            if self.running:
                self.letters_frame.place(relx=0.1, rely=0.25)
                self.score_frame.place(x=560, y=120)
                self.found_words_frame.place(x=550, y=250)
                # self.msg_to_print_label.place(x=320, y=100)
        self.is_exit_pressed = False

    def starting_board_graphics(self):
        """Initializes the graphics of the game to the screen - places all
        buttons and frames in their place"""
        self.root.resizable(False, False)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.geometry('700x700')
        self.root.title('Boggle')
        self.boggle_title.config(text="Are you ready to BOGGLE???", font=("MS "
                                "Serif", 30, "bold"), fg="white", bg="black")
        self.boggle_title.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        self.instructions_button.place(relx=0.375, rely=0.3)
        self.start_button.config(text='Start', command=self.start,
                                 font=("Times New Roman", 20, "bold"),
                                 fg="MistyRose2", bg='maroon', height=1,
                                 width=7, borderwidth=10)
        self.start_button.pack()
        self.time_frame.config(highlightthickness=3, highlightbackground=
                            "MediumPurple3", text="Time Left", font=("Times "
                            "New Roman",16, "bold"), cursor="watch",
                            bg="MediumPurple1")
        self.time_label.config(bg="MediumPurple1")
        self.time_label.pack()
        self.score_frame.config(bg="MediumPurple1", highlightbackground=
                                "MediumPurple3", highlightthickness=3,
                                height=50, width=70, text='Score', font=
                                ("Times New Roman",16, "bold"))
        self.score_label.config(bg="MediumPurple1", height=2, width=10,
                                fg='black', font=("Times New Roman",16))
        self.exit_button.place(relx=1, x=-2, y=2, anchor=tk.NE)

    def get_is_not_pressed(self):
        """Returns information about the mouse"""
        return self.is_not_pressed

    def _draw_letters(self):
        """Draws the letters to the screen"""
        self.letters_frame = tk.Frame(self.canvas, bg="")
        self.letters_frame.place(relx=0.1, rely=0.25)
        # self.msg_to_print_label.place(x=320, y=100)
        for i, row in enumerate(self.board):
            buttons_row = []
            for j, col in enumerate(row):
                button = Buttons(self.letters_frame, col, i, j)
                buttons_row.append(button)
                button.get_button().grid(row=i, column=j, padx=12, pady=12)
            self.buttons_list.append(buttons_row)

    def add_found_word(self, word):
        """Prints the good word to the screen (inside the found_words_list"""
        self.found_words_list.insert(0, word) #each new word - insert to the *top* of the list

    def motion(self):
        """This function is called when there is a motion over the buttons on
        the board, adds the letters of the touched buttons to the current
        formulated word, (if the button hasn't been touched already), or
        deletes letters from the word when moving back and resets the word if
        the move is illegal"""
        def func_motion(event):
            for i, row in enumerate(self.buttons_list):
                for j, button in enumerate(row):
                    if button.get_button().winfo_containing(event.x_root,
                                                            event.y_root) is button.get_button():
                        if self.Pressed_Buttons:
                            if not self.legal_move(i, j,
                                                   self.Pressed_Buttons[-1]):
                                self.no_motion()(None)
                                self.saved_word = ""
                                continue
                        if button not in self.Pressed_Buttons:
                            self.Pressed_Buttons.append(button)
                            self.current_word += button.get_text()
                        else:
                            self.Pressed_Buttons = self.Pressed_Buttons[
                                                   :self.Pressed_Buttons.index(
                                                       button) + 1]
                            self.current_word = self.current_word[
                                                :self.current_word.rindex(
                                                    button.get_text()) + len(
                                                    button.get_text())]
                        self.keep_pressed_down()

        return func_motion

    def keep_pressed_down(self):
        """Sets all buttons in self.pressed_buttons to look as if they are
        pressed"""
        for row in self.buttons_list:
            for button in row:
                if button in self.Pressed_Buttons:
                    button.get_button().config(relief=tk.SUNKEN,
                                               bg='SpringGreen3')
                else:
                    button.get_button().config(relief=tk.RAISED,
                                               bg='pale goldenrod')

    def legal_move(self, i, j, previous_button):
        """Checks if a move on the board is legal
        :param i: new row
        :param j: new column
        :param previous_button
        :return: True if the move to (i,j) is legal - next to the previous
         button
        """
        prev_row, prev_col = previous_button.get_row(), previous_button.get_col()
        possible_moves = [(prev_row - 1, prev_col - 1),
                          (prev_row - 1, prev_col),
                          (prev_row - 1, prev_col + 1),
                          (prev_row, prev_col - 1),
                          (prev_row, prev_col + 1),
                          (prev_row, prev_col),
                          (prev_row + 1, prev_col - 1),
                          (prev_row + 1, prev_col),
                          (prev_row + 1, prev_col + 1)]
        if 0 <= i < len(self.buttons_list) and 0 <= j <= len(
                self.buttons_list[0]) and ((i, j) in possible_moves):
            return True
        return False

    def no_motion(self):
        """This function is called when there is no motion on the buttons of
        the board, saves the formulated word to self.saved_word and
        resets all pressed buttons and self.current_word"""
        def func_no_motion(event):
            self.saved_word = self.current_word
            for button in self.Pressed_Buttons:
                button.get_button().config(relief=tk.RAISED,
                                           bg='pale goldenrod')
            self.Pressed_Buttons = []
            self.is_not_pressed = True
            self.current_word = ""
        return func_no_motion

    def get_saved_word(self):
        """A getter of the formed word, the Game uses it to check if
        the word exists in the boggle_dict"""
        return self.saved_word

    def run_board(self):
        """Checks if there is mouse motion over the buttons and calls the
        relevant function"""
        if self.root:
            if self.running:
                function_motion = self.motion()
                function_no_motion = self.no_motion()
                self.root.bind_all("<B1-Motion>", function_motion)
                self.root.bind_all("<ButtonRelease-1>",
                                   function_no_motion)  # once the mouse is no
            # longer pressed
        else:
            exit()

    def timer(self, minutes, seconds):
        """Gets time from the Game and prints to the screen"""
        if minutes == 0 and int(seconds) <= 10 and int(
                seconds) % 2 == 0:  # make the bg red-black when there are
            # 10 secs left
            self.time_label.config(fg="red", text=str(minutes).zfill(1) + ':' + str(seconds).zfill(2), font=("Times New Roman",16))
            self.time_frame.config(fg="red")
        else:
            self.time_label.config(fg="black", text=str(minutes).zfill(1) + ':' + str(seconds).zfill(2),
                                   font=("Times New Roman",16))
            self.time_frame.config(fg="black")

    def start(self):
        """This function is called when a new game starts,
        resets all widgets on the board"""
        self.instructions_button.place_forget()
        self.time_frame.place(x=578, y=50)
        self.score_frame.place(x=560, y=120)
        self.score_label.pack()
        self.board = boggle_board_randomizer.randomize_board()
        self.running = True
        self._draw_letters()
        self.boggle_title.place_forget()
        self.start_button.config(text='Restart', command=self.end, height=1,
                                 width=7, font=("Times New Roman",20, "bold"))
        self.start_words_frame()

    def start_words_frame(self):
        """Resets all tkinter widgets related to the found words frame"""
        self.found_words_frame = tk.Frame(self.canvas)
        self.found_words_list = tk.Listbox(self.found_words_frame, bg='MediumPurple1', bd=5)
        self.scroll_bar = tk.Scrollbar(self.found_words_frame)
        self.found_words_frame.place(x=550, y=250)
        title = tk.Label(self.found_words_frame, text='Found Words', font=("Times New Roman",16, "bold"))
        title.pack(side=tk.TOP)
        self.found_words_list.pack(side=tk.LEFT)
        self.scroll_bar.config(command=self.found_words_list.yview)
        self.scroll_bar.pack(side=tk.RIGHT, fill='both')

    def end(self, winning=True):
        """This function is called when a game ends, it removes all game
        widgets and shows a relevant massage according to winning or losing"""
        self.running = False
        self.time_frame.place_forget()
        self.time_label.pack_forget()
        self.letters_frame.destroy()
        self.score_frame.place_forget()
        self.buttons_list = []
        self.found_words_frame.destroy()
        self.Pressed_Buttons = []
        self.start_button.config(text='Start', command=self.start, height=1,
                                 width=7, borderwidth=10, font=("Times New Roman",20, "bold"))
        self.boggle_title.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        self.instructions_button.place(relx=0.375, rely=0.3)
        if not winning:
            messagebox.showinfo('Game Over', "Time is up, your score is: " + str(self.score_label.cget("text")))
        else:
            messagebox.showinfo('Game Ended', "Menu")

    def get_running(self):
        return self.running

    def set_score(self, score):
        self.score_label.config(text=str(score))
