'''Create a random three line linear drum groove.
   Subdivisions can be 1, 2, 3, or 4...
   (quarter notes, eighth notes, triplets, sixteenth notes)'''
import random

def separate(notes):
    '''Splits a one-line groove into three separate lines'''
    for item in notes:
        if item == "H":
            hh.append("H")
            kick.append(" ")
            snare.append(" ")
        elif item == "K":
            kick.append("K")
            snare.append(" ")
            hh.append(" ")
        else:
            snare.append("S")
            kick.append(" ")
            hh.append(" ")
    return

def set_grid(subdivision):
    '''Set the subdivision of the groove based on user's input'''
    grid = ""

    if subdivision == 1:
        grid = "1 2 3 4"
    elif subdivision == 2:
        grid = "1 + 2 + 3 + 4 +"
    elif subdivision == 3:
        grid = "1 t l 2 t l 3 t l 4 t l"
    elif subdivision == 4:
        grid = "1 e + a 2 e + a 3 e + a 4 e + a"

    return grid

def print_notes():
    '''Prints the grid and a separate line for each instrument'''
    print(grid)
    print(" ".join(hh))
    print(" ".join(snare))
    print(" ".join(kick))


if __name__ == "__main__":
    hh = []
    kick = []
    snare = []
    possibilites = ["H", "S", "K"]

    # Ask user input for subdivision
    subdivision = int(input("Select a grid subdivision to use (1/2/3/4): "))

    # Set the grid according to the subdivision
    grid = set_grid(subdivision)

    # Populate the notes array with placeholders
    notes = [0] * (subdivision * 4)

    # Populate the notes array with random notes
    for i in range(len(notes)):
        notes[i] = random.choice(possibilites)

    # Separate notes into three lines
    separate(notes)

    print_notes()
