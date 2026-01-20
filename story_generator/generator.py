import random
import os

is_first_call = True

def story(n):
    """
    Simulates a dungeon adventure with various random encounters. 
    Input: 
        file_name (int): number of encounters the 
        adventurer will run into.
    Returns:
        None
    """
    global is_first_call
    if is_first_call == True:
        print("You enter the dungeon...")
        is_first_call = False

    if n <= 0:  # Reject non-positive input
        return

    else:
        # Each item corresponds to a certain 'encounter' function call
        encounters = ["stairs", "treasure", "mirror", "stranger"]
        encounter = random.choice(encounters)

        if encounter == "stairs":
            confirm_yes = input(
                "You've found some descending stairs, would you like to go down? "
            )
            if confirm_yes.lower() == "yes" or confirm_yes.lower() == "y":
                number_stairs = random.choice(list(range(1, 11)))
                stairs(number_stairs)
            else:
                print("You choose not to go down.")

        elif encounter == "treasure":
            # Sample probabilities (90% square, 10% diamond)
            sample_set = 9 * ["square"] + 1 * ["diamond"]
            drawn_treasure = random.choice(sample_set)

            if drawn_treasure == "square":
                print("You found a square gem!")
                square_size = random.choice(list(range(1, 6)))
                square(square_size)
            if drawn_treasure == "diamond":
                print("You found a rare diamond!")
                diamond_size = random.choice(list(range(1, 16)))
                diamond(diamond_size)

        elif encounter == "mirror":
            user_string = input(
                "You've found the mirror realm! Anything you say will be reversed, try it out: "
            )
            mirror(user_string)

        elif encounter == "stranger":
            print("You come across a mysterious stranger, he warns you that...")
            base_dir = os.path.dirname(__file__)
            grammar_path = os.path.join(base_dir, "grammar.txt")
            dictionary = generate_structure(grammar_path)
            generate_sentence("<s>", dictionary)
            print("")

    return story(n - 1)


def stairs(levels: int):
    """
    Prints out a set of stairs using the ▅ character.
    Input:
        levels (int): the number of levels to be drawn.
    Returns:
        None
    """
    if levels <= 0:  # Reject non-positive input
        return
    else:
        # Base case: one level
        if levels == 1:
            print("\u2585")
            return
        else:
            stairs(levels - 1)
            print(levels * "\u2585")


def square(length: int, state=1):
    """
    Prints out a square using the ◆ character.
    Input:
        length (int): the number of units on a side.
        state (int): default parameter to track state (internal use).
    Returns:
        None
    """
    if length <= 0:
        return
    else:
        # Base case: iteration equals requested length
        if state == length:
            print(length * "\u25c6")  # Top line of square
            return
        else:
            square(length, state + 1)

            if state == 1:  # Bottom line of square
                print(length * "\u25c6")
            else:
                # Padding in middle of square
                print("\u25c6" + (length - 2) * " " + "\u25c6")


def diamond(length, state=0):
    """
    Prints out a diamond using the * character.
    Input:
        length (int): Must be a positive odd integer (vertical length).
        state (int): Tracks recursion depth (internal use).
    Returns:
        None
    """
    if length <= 0 or (length % 2) == 0:
        return

    else:
        # Number of whitespaces to the left of the
        # axis of symmetry of diamond
        middle_position = (length - 1) // 2

        # Base case: requested length reached (tip of diamond)
        if state == length - 1:
            print(middle_position * " " + "*" + middle_position * " ")
            return

        else:
            diamond(length, state + 1)

            if state == 0:  # Bottom point of diamond
                print(middle_position * " " + "*" + middle_position * " ")

            else:
                # Top half of diamond
                if state > middle_position:
                    # Converting state to equivalent n for calculation
                    state = (2 * middle_position) - state

                # Calculate required whitespace inside indent
                padding_value = (2 * state) - 1
                padding = padding_value * " "

                # Calculate required whitespace outside indent
                indent_value = (length - (padding_value + 2)) // 2
                indent = indent_value * " "

                print(indent + "*" + padding + "*" + indent)


def mirror(string_input: str):
    """
    Prints out the reverse of a string.
    Input:
        string_input (str): The string to be printed in reverse order.
    Returns:
        None
    """
    characters = list(string_input)

    # Base case: if the list of characters is empty
    # (all characters have been processed), print a newline and return
    if characters == []:
        print("")
        return
    else:
        # Remove last character and print it without newline
        print(characters.pop(-1), end="")

        # Recursive call for the remaining characters
        remaining_string = "".join(characters)
        mirror(remaining_string)


def generate_structure(file_name: str) -> dict:
    """
    Reads the sentence structure from a file and
    represents it in a dict.
    Input:
        file_name (str): File from which dictionary
        format will be extracted.
    Returns:
        structure (dict): Dictionary representing
        sentence structure from file.
    """
    structure = {}
    file_object = open(file_name, "r")

    for line in file_object.readlines():
        stripped = line.strip()

        splitted = stripped.split(":")
        # The first part is the key, separated by ':'
        key = splitted[0]
        # The second part is the value, separated by '|'
        value = splitted[1].split("|")

        # Assign the key-value pair to the structure dictionary
        structure[key] = value

    file_object.close()
    return structure


def generate_sentence(symbol, structure):
    """
    Prints a random sentence from a provided
    dictionary structure.
    Input:
        symbol (str): The symbol to look at in the structure.
        structure (dict): A dictionary presenting
        sentence strucutre.
    Returns:
        None
    """
    # Retrieve corresponding values from symbol
    values = structure.get(symbol)
    # Randomly pick one item from symbol values
    choice = random.choice(values)
    splitted = choice.split(",")

    for part in splitted:
        if "<" not in part:  # When non-terminal reached
            print(part, end=" ")
            continue  # Move to adjacent symbol
        else:
            # Break down terminals further
            generate_sentence(part, structure)

if __name__ == "__main__":
    # Change this to the number of levels you want
    story(3)