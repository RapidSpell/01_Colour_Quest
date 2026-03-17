from tkinter import *


class Converter:
    """
    Temperature conversion tool ( Celsius to Fahrenheit or vice versa )
    """

    def __init__(self):
        """
        Initialise the colour quest
        """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # strings for labels
        self.intro_string = ("In each round you will be invited to chose a "
                       "colour. Your goal is to beat the target score "
                       "and win the round (and keep your points)")

        # chose_string = "opps - please chose a whole number more than zero."
        self.choose_string = "how many rounds would you like to play?"
        self.choose_txt_colour = "#009900"

        # list of variables to make (text | font | fg)
        start_labels_list = [
            ["Colour Quest", "Arial 16 bold", None, 0],
            [self.intro_string, "Arial 12", None, 1],
            [self.choose_string, "Arial 14", self.choose_txt_colour, 2],
        ]

        # list to hold labels after they have been made
        self.label_ref_list = []

        # Create labels and add them to the reference list
        for item in start_labels_list:
            self.make_label = Label(self.start_frame, text=item[0],
                                    font=item[1], fg=item[2], wraplength=400)
            self.make_label.grid(row=item[3])

            self.label_ref_list.append(self.make_label)

        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds = Entry(self.entry_area_frame, font="Arial 19")
        self.num_rounds.grid(row=0, column=0)

        self.play_button = Button(self.entry_area_frame, text="Play",
                                  font=("Arial", 12, "bold"), fg="#ffffff",
                                  bg="#0057D8", width=10,
                                  command=self.to_play)
        self.play_button.grid(row=0, column=1)


    def to_play(self):
        """Retrieves the value from the associated Tkinter variable."""
        # Access the value directly from the Tkinter variable
        try:
            rounds = int(self.num_rounds.get())

            if 0 < rounds < 100:
                # set label back to standard so if they come back to the
                # round select page it will not still be red
                self.label_ref_list[2].config(text=self.choose_string,
                                              fg=self.choose_txt_colour, font="Arial 14 bold")

                # send user to PlayGame class to start the game
                PlayGame(rounds)

                # remove box for number of games select
                root.withdraw()

            else:
                # change the text and change colour to red for the error message
                self.label_ref_list[2].config(text="Please enter an integer between 1 and 100",
                                              fg="#880808", font="Arial 14 bold")

        except ValueError:
            # change the text and change colour to red for the error message
            self.label_ref_list[2].config(text="Please enter a Valid integer", fg="#880808",
                                          font="Arial 14 bold")


class PlayGame:
    """
    runs game
    """

    def __init__(self, num_games):
        """
        create the game GUI the game
        """

        # setup dialogue box
        self.play_box = Toplevel()

        # set constant button width
        self.button_width = 20

        self.play_frame = Frame(self.play_box, padx=10, pady=10)
        self.play_frame.grid()

        # create frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.play_frame, width=self.button_width)
        self.hints_stats_frame.grid(row=6, column=0)

        # Create frame to hold colour select buttons
        self.colour_frame = Frame(self.play_frame, width=self.button_width)
        self.colour_frame.grid(row=2)

        # create variable to track how many rounds left to play
        temp_games = num_games

        # while loop to continue to play rounds until no more rounds left
        while temp_games > 0:

            # change games left counter
            temp_games -= 1

            # identify what the score to beat is
            self.score_to_beat = "#"

            # create games played label
            self.games_label = (f"Round {num_games - temp_games} of {num_games}\n"
                                f"You Have {temp_games} rounds left")

            # Create label show what game number they are on
            self.play_label = Label(self.play_frame, text=self.games_label, fg="#000000", font="Arial 14")
            self.play_label.grid(row=0, column=0)

            # create label to show the score to beat
            self.beat_score_label = Label(self.play_frame, text=f"sore to beat = {self.score_to_beat}",
                                          fg="#000000")
            self.beat_score_label.grid(row=1)

            # Create color select options
            self.colour_1 = "Colour 1"
            self.colour_2 = "Colour 2"
            self.colour_3 = "Colour 3"
            self.colour_4 = "Colour 4"

            # list to create colour select buttons from
            # Text | bg Colour | Row | Column | Command

            colour_button_list = [
                [self.colour_1, "#000000", 0, 0],
                [self.colour_2, "#000000", 0, 1],
                [self.colour_3, "#000000", 1, 0],
                [self.colour_4, "#000000", 1, 1]
            ]

            for colour_item in colour_button_list:
                self.colour_buttons = Button(self.colour_frame, text=colour_item[0], fg="#ffffff",
                                             bg=colour_item[1], width=9, font="Arial 16 bold", # command goes here
                                             )
                self.colour_buttons.grid(row=colour_item[2], column=colour_item[3], padx=5, pady=5)

            # create result label
            self.result_label = Label(self.play_frame, text="You Chose, Result", fg="#000000",
                                      font="Arial 12")
            self.result_label.grid(row=3, column=0)

            # if they are not on their last round show the next round button
            if temp_games == 0:
                self.make_next_button = "No"

            else:
                self.make_next_button = "Yes"

            # list to create the buttons from
            # [Make buton yes/no | Frame | Text | Width | Background | Row | Column | Command
            make_buttons_list = [
                [self.make_next_button, self.play_frame, "Next Round", self.button_width, "#0057d8", 5, 0, self.next_round],
                ["Yes", self.hints_stats_frame, "Hints", 9, "#ff8000", 1, 0, self.to_hints],
                ["Yes", self.hints_stats_frame, "Stats", 9, "#333333", 1, 1, self.to_stats],
                ["Yes", self.play_frame, "End Game", self.button_width, "#990000", 7, 0, self.close_play],
            ]

            # List to hold buttons after they are created
            self.button_ref_list = []

            # create the buttons using the values from make_buttons_list
            for item in make_buttons_list:
                if item[0] == "Yes":
                    self.make_button = Button(item[1], text=item[2], fg="#000000",
                                              width=item[3], bg=item[4], font="Arial 16 bold",
                                              command=item[7])
                    self.make_button.grid(row=item[5], column=item[6], padx=5, pady=5)

                    self.button_ref_list.append(self.make_button)

            # Name the buttons
            if self.make_next_button == "Yes":
                self.next_button = self. button_ref_list[0]
                self.hints_button = self.button_ref_list[1]
                self.stats_button = self.button_ref_list[2]
                self.end_game_button = self.button_ref_list[3]

    def close_play(self):
        # open number of games select tab
        root.deiconify()

        # close game tab
        self.play_box.destroy()


    def next_round(self):
        """" this function takes you to the next round """


    def to_hints(self):
        """ this function sends you to the hint page """


    def to_stats(self):
        """ this function sends you to the stats page """


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest (not responding)")
    Converter()
    root.mainloop()
