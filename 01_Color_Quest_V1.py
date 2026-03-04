from tkinter import *


class Converter:
    """
    Temperature conversion tool ( Celsius to Fahrenheit or vice versa )
    """

    def __init__(self):
        """
        Initialise the colour quest
        """
        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()

        self.temp_heading = Label(self.temp_frame,
                                  text="Colour Quest", font=("Arial", 14, "bold"))
        self.temp_heading.grid(row=0)

        self.temp_instructions = Label(self.temp_frame,
                                       text="In each round you will be invited to chose a"
                                            "colour. Your goal is to beat the target score"
                                            "and win the round (and keep your points)",
                                       font=("Arial", 12), wraplength=400)
        self.temp_instructions.grid(row=1)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("colour quest")
    Converter()
    root.mainloop()
