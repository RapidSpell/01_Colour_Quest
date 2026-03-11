from tkinter import *
from functools import partial # To prevent unwanted windows


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

        self.num_rounds = Spinbox(self.entry_area_frame, from_=1, to=100)
        self.num_rounds.grid(row=0, column=0)

        self.play_button = Button(self.entry_area_frame, text="Play",
                                        font=("Arial", 12, "bold"),
                                        fg="#ffffff", bg="#0057D8", width=10,
                                        command=self.to_play)
        self.play_button.grid(row=0, column=1)


    def to_play(self):
        """Retrieves the value from the associated Tkinter variable."""
        # Access the value directly from the Tkinter variable
        try:
            rounds = int(self.num_rounds.get())

            if 0 < rounds < 100:
                # send user to PlayGame class to start the game
                PlayGame(rounds)

                # remove box for number of games select
                root.withdraw()

            else:

                self.label_ref_list[2].config(text="Please enter an integer between 1 and 100",
                                              fg="#880808", font="Arial 14 bold")

        except ValueError:
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
        self.game_box = Toplevel()

        self.play_frame = Frame(padx=10, pady=10)
        self.play_frame.grid()

        self.temp_num_games = num_games

        while self.temp_num_games > 0:

            # create games played label
            self.games_label = (f"Round {self.temp_num_games} of {num_games}\n"
                                f"You Have {num_games - self.temp_num_games} "
                                f"rounds left")

            # Create label show what game number they are on
            self.play_label = Label(self.play_frame, text=self.games_label, fg="#000000", font="Arial 14")
            self.play_label.grid(row=0, column=0)

            # change games left counter
            self.temp_num_games -= 1

        root.mainloop()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest (not responding)")
    Converter()
    root.mainloop()
