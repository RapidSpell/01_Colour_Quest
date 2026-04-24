from tkinter import *
import csv
import random
from functools import partial


# Helper functions go here
def round_ans(val):
    """
    Round numbers to the nearest integer.
    :param val: number to be rounded
    :return:  number (an integer)
    """
    var_rounded = (val * 2 + 1) // 2
    raw_rounded = "{:.0f}".format(var_rounded)
    return int(raw_rounded)


def get_colours():
    """
    retries colours from csv file
    :return: list of colours where each item has the colour name, associated score and foreground colour for the text
    """

    file = open("colour_list_hex_v3.csv", "r")
    all_colours = list(csv.reader(file, delimiter=","))
    file.close()

    # remove the first row
    all_colours.pop(0)

    return all_colours


def get_round_colours():
    """
    Choose four colours from larger list ensuring that the scores are all different.
    :return: list of colours and score to beat (median of scores)
    """

    all_colours_list = get_colours()

    round_colours = []
    colour_scores = []

    # loop until we have 4 colours with different scores
    while len(round_colours) < 4:
        potential_colour = random.choice(all_colours_list)

        # Get the score and check it is not a duplicate
        if potential_colour[1] not in colour_scores:
            round_colours.append(potential_colour)
            colour_scores.append(potential_colour[1])

    # Change scores to integers
    int_scores = [int(x) for x in colour_scores]
    int_scores.sort()

    # get median score/target score
    midian = (int_scores[1] + int_scores[2]) / 2
    midian = round_ans(midian)
    highest = int_scores[-1]

    return round_colours, midian, highest


# Classes start here
class StartGame:
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

            if 0 < rounds <= 100:
                # set label back to standard so if they come back to the
                # round select page it will not still be red
                self.label_ref_list[2].config(text=self.choose_string,
                                              fg=self.choose_txt_colour, font="Arial 14 bold")

                self.num_rounds.config(bg="#ffffff")

                # send user to PlayGame class to start the game
                PlayGame(rounds)

                # remove box for number of games select
                root.withdraw()

            else:
                # change the text and change colour to red for the error message
                self.label_ref_list[2].config(text="Please enter an integer between 1 and 100",
                                              fg="#880808", font="Arial 14 bold")

                self.num_rounds.config(bg="#f4cccc")

        except ValueError:
            # change the text and change colour to red for the error message
            self.label_ref_list[2].config(text="Please enter a Valid integer", fg="#880808",
                                          font="Arial 14 bold")

            self.num_rounds.config(bg="#f4cccc")


class PlayGame:
    """
    runs game
    """

    def __init__(self, num_games):
        """
        create the game GUI
        """

        # Integers / String Variables
        self.num_games = num_games

        self.target_score = IntVar()

        # rounds left - initialize it as num rounds when first round is played
        self.rounds_left = IntVar()
        self.rounds_left.set(num_games)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(num_games)

        self.round_score = IntVar()
        self.round_score.set(0)

        # initialize lists needed for colour storage etc
        self.round_colour_list = []
        self.all_scores_list = []
        self.all_medians_list = []

        # setup dialogue box
        self.play_box = Toplevel()

        # set constant button width
        self.button_width = 39

        self.play_frame = Frame(self.play_box, padx=10, pady=10)
        self.play_frame.grid()

        # Create frame to hold colour select buttons
        self.colour_frame = Frame(self.play_frame, width=self.button_width)
        self.colour_frame.grid(row=2)

        self.colour_button_ref = []
        self.button_colours_list = []

        # create games played label
        self.games_label_update = (f"Round {self.num_games - self.rounds_left.get()} of {self.num_games}\n"
                                   f"You Have {self.rounds_left.get()} rounds left")

        # Create label show what game number they are on
        self.play_label = Label(self.play_frame, text=self.games_label_update, fg="#000000", font="Arial 18")
        self.play_label.grid(row=0, column=0)

        # create label to show the score to beat
        self.beat_score_label = Label(self.play_frame, text=f"sore to beat",
                                 fg="#000000", font="Arial 14 bold")
        self.beat_score_label.grid(row=1)

        # create four buttons in a 2 x 2 grid
        for item in range(0, 4):
            self.colour_button = Button(self.colour_frame, font="Arial 12",
                                        text="Colour Name", width=15,
                                        command=partial(self.round_results, item))
            self.colour_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5, pady=5)

            self.colour_button_ref.append(self.colour_button)

        # create result label
        self.result_label = Label(self.play_frame, text="", fg="#000000",
                             font="Arial 12")
        self.result_label.grid(row=3, column=0)

        self.hints_stats_frame = Frame(self.play_frame)
        self.hints_stats_frame.grid(row=6)

        # list to create the buttons from
        # [Make buton yes/no | Frame | Text | Width | Background | Row | Column | Command
        make_buttons_list = [
            ["No", self.play_frame, "Next Round", self.button_width, "#0057d8", 5, 0, self.new_round],
            ["No", self.hints_stats_frame, "Hints", 18, "#ff8000", 1, 0, self.to_hints],
            ["No", self.hints_stats_frame, "Stats", 18, "#333333", 1, 1, self.to_stats],
            ["No", self.play_frame, "End Game", self.button_width, "#990000", 7, 0, self.close_play],
        ]

        self.button_ref_list = []

        # create the buttons using the values from make_buttons_list
        for item in make_buttons_list:
            make_button = Button(item[1], text=item[2], fg="#000000",
                                      width=item[3], bg=item[4], font="Arial 16 bold",
                                      command=item[7])
            make_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            self.button_ref_list.append(make_button)

        self.next_button = self.button_ref_list[0]

        self.to_hints_button = self.button_ref_list[1]

        # disable stats button
        self.to_stats_button = self.button_ref_list[2]
        self.to_stats_button.config(state="disabled")

        self.new_round()


    def new_round(self):
        """"
        this function configures all the labels and
        buttons for the next round
        """
        # create variable to track how many rounds left to play
        temp_games = self.rounds_left.get()

        if temp_games > 0:
            # change games left counter
            temp_games -= 1
            self.rounds_left.set(temp_games)

            # identify what the score to beat is
            self.round_colour_list, median, highest = get_round_colours()
            self.target_score.set(median)

            self.beat_score_label.config(text=f"Target score: {median}")


            for count, item in enumerate(self.colour_button_ref):
                item.config(fg=self.round_colour_list[count][2],
                            bg=self.round_colour_list[count][0],
                            text=self.round_colour_list[count][0], state=NORMAL)

            self.result_label.config(text="You Chose, Result")

            if self.rounds_left.get() == 0:
                self.next_button.config(state="disabled", text="(This is your last round!)",
                                   fg="#990000")

            else:
                self.next_button.config(state="disabled", text="Next Round",
                                        fg="#990000")

            self.play_label.config(text=f"Round {self.num_games - self.rounds_left.get()} of {self.num_games}\n"
                                   f"You Have {self.rounds_left.get()} rounds left")


    def round_results(self, user_choice):
        """
        retrieves which button was pressed (Index 0 - 3), retrieves
        score and compares it with median, updates results and add results to stats page
        """
        # get user score and colour based on button press...
        score = int(self.round_colour_list[user_choice][1])

        colour_name = self.colour_button_ref[user_choice].cget('text')

        target = self.target_score.get()

        # retrieve target score and compare with user score to find round result target = self.target_score.get()
        if score >= target:
            result_text = f"Success! {colour_name} earned you {score} points"
            result_bg = "#82B366"

            self.round_score.set(self.round_score.get() + score)

        else:
            result_text = f"Oops {colour_name} ({score}) is less than the target."
            result_bg = "#F8CECC"

        self.result_label.config(text=result_text, bg=result_bg)

        for item in self.colour_button_ref:
            item.config(state="disabled")

        self.to_stats_button.config(state="normal")

        if self.rounds_left.get() > 0:
            self.next_button.config(state="normal", text="Next Round",
                                    fg="#000000")


    def close_play(self):
        # open number of games select tab
        root.deiconify()

        # close game tab
        self.play_box.destroy()


    def to_hints(self):
        """ this function sends you to the hint page """

        DisplayHints(self)

        # Disable help button
        self.to_hints_button.config(state=DISABLED)


    def to_stats(self):
        """ this function sends you to the stats page """


class DisplayHints:

    def __init__(self, partner):

        # setup dialogue box and background color
        background = "#FFE6CC"
        self.help_box = Toplevel()

        # Disable help button
        partner.to_hints_button.config(state=DISABLED)

        # if users press cross at the top, coses help and
        # 'releases' help button
        self.help_box.protocol("WM_DELETE_WINDOW",
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box,
                                height=200)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                        text="Help / Info",
                                        font=("Arial", 14, "bold"),)
        self.help_heading_label.grid(row=0)

        help_text = """
The score for each colour relates to it's hexadecimal code.

Remember, the hex code for white is #FFFFFF - which is the best possible score.

The hex code for black is #000000 which is the worst possible score.

The first colour in the code is red, so if you had to choose between red (#FF0000), green (#00FF00) and blue (#0000FF), then red would be the best choice.

Good luck!
        """

        self.help_text_label = Label(self.help_frame,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", 12, "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # List and loop to set background color on
        # everything except the buttons
        recolor_list = [self.help_frame, self.help_heading_label,
                        self.help_text_label]

        for item in recolor_list:
            item.config(bg=background)


    def close_help(self, partner):
        """
        Closes help dialogue box (and enables help button)
        """
        # Put help button back to normal...
        partner.to_hints_button.config(state=NORMAL)
        self.help_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest (not responding)")
    StartGame()
    root.mainloop()
