from tkinter import *

from click import command


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
        self.intro_string = ("In each round you will be invited to chose a"
                       "colour. Your goal is to beat the target score"
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

        self.num_rounds_button = Button(self.entry_area_frame, text="Play",
                                        font=("Arial", 12, "bold"),
                                        fg="#ffffff", bg="#0057D8", width=10,
                                        command=self.to_play)
        self.num_rounds_button.grid(row=0, column=1)


    def to_play(self):
        """Retrieves the value from the associated Tkinter variable."""
        # Access the value directly from the Tkinter variable
        rounds = self.num_rounds.get()
        try:
            rounds = int(rounds)

            if 0 < rounds < 100:
                PlayGame(self, self.num_rounds)

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
    def __init__(self, partner, num_games):
        print(num_games)



# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest (not responding)")
    Converter()
    root.mainloop()
