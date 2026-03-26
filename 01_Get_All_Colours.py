import csv
import random

def round_ans(val):
    """
    Round numbers to the nearest integer.
    :param val: number to be rounded
    :return:  number (an integer)
    """
    var_rounded = (val * 2 + 1) // 2
    raw_rounded = "{:.0f}".format(var_rounded)
    return int(raw_rounded)


# Retrieve colours from csv and put them into a list
file = open("colour_list_hex_v3.csv", "r")
all_colours = list(csv.reader(file, delimiter=","))
file.close()

# remove the first row
all_colours.pop(0)

round_colours = []
colour_scores = []

# loop until we have 4 colours with different scores
while len(round_colours) < 4:
    potential_colour = random.choice(all_colours)

    # Get the score and check it is not a duplicate
    if potential_colour[1] not in colour_scores:
        round_colours.append(potential_colour)
        colour_scores.append(potential_colour[1])

print(round_colours)
print(colour_scores)

# Find target score (median)

# Change scores to integers
int_scores = [int(x) for x in colour_scores]
int_scores.sort()

midian = (int_scores[1] + int_scores[2]) / 2
midian = round_ans(midian)
print("midian rounded", midian)