class Exercise:
    def __init__(self, name, distance, duration, date):
        self.name = name
        self.distance = float(distance)
        self.duration = int(duration)
        self.date = date

    def get_name(self):
        return self.name

    def get_distance(self):
        return self.distance

    def get_duration(self):
        return self.duration

    def get_date(self):
        return self.date


class User:
    def __init__(self, username):
        self.username = username
        # intialise empty list of exercises to add to 
        # later from file data
        self.exercises = []

    def get_username(self):
        return self.username

    def get_exercises(self):
        return self.exercises

    def read_data(self):
        filename = self.username + ".txt"

        try:
            file_object = open(filename, "r")
        except FileNotFoundError:
            print(f"{self.username} has no available data.")
            return False

        for line in file_object.readlines():
            # Remove any extra whitespaces in line
            stripped = line.strip()
            # Split data in line to assign to fields later
            fields = stripped.split(",")

            # Skip invalid or blank lines
            if len(fields) != 4:
                continue
            else:
                # Create an Exercise object from fields and
                # add to the exercises list
                name, distance, duration, date = fields
                item = Exercise(name, distance, duration, date)
                self.exercises.append(item)

        file_object.close()
        return True

    def calculate_distance(self, exercise_name, month):
        total_distance = 0

        for exercise in self.exercises:
            # Calculate total distance for given exercise name
            if month == None and exercise.name == exercise_name:
                total_distance += exercise.distance

            # Calculate total distance for given exercise name and month
            if exercise.name == exercise_name and exercise.date == month:
                total_distance += exercise.distance

        return total_distance

    def calculate_max_distance(self, exercise_name):
        max_distance = 0
        # Find the greatest distance in the exercises list
        for exercise in self.exercises:
            if exercise.name == exercise_name and exercise.distance > max_distance:
                max_distance = exercise.distance

        return max_distance

    def calculate_duration(self, exercise_name, month):
        total_duration = 0

        for exercise in self.exercises:
            # Calculate total duration for the given exercise name
            if month == None and exercise.name == exercise_name:
                total_duration += exercise.duration

            # Calculate total duration for given exercise name and month
            if exercise.name == exercise_name and exercise.date == month:
                total_duration += exercise.duration

        return total_duration

    def calculate_max_duration(self, exercise_name):
        max_duration = 0
        # Find the greatest duration in the exercises list
        for exercise in self.exercises:
            if exercise.name == exercise_name and exercise.duration > max_duration:
                max_duration = exercise.duration

        return max_duration

    def count_matching_data(self, exercise_name, month):
        count = 0
        # Count occurence of given exercise name
        for exercise in self.exercises:
            if month == None and exercise.name == exercise_name:
                count += 1
            # Count occurence of given exercise name and month
            if exercise.name == exercise_name and exercise.date == month:
                count += 1
        return count


def welcome_screen():
    # this is the line on the top, middle
    # and bottom of the screen
    line = 13 * "*-" + "*"

    # this prints out all of the lines to form the screen
    print(line)
    print("| WELCOME TO USYD FITNESS |")
    print(line)
    print("*    LOGS YOUR WORKOUT    *")
    print("*   TRACKS YOUR FITNESS   *")
    print("*    GET FIT & HEALTHY    *")
    print(line)

    return


def login():
    line = 27 * "~"  # this forms the horizontal borders

    username = str(input("Login with your username: "))
    length_name = len(username)

    if length_name > 20:
        print("Your username is too long.")
        return None

    else:

        # determine whitespaces needed for user greeting line
        whitespace = (27 - (length_name + 6)) * " "

        print(line)
        print(f"| Hi {username}{whitespace}|")
        print(line)
        print("| [1] Log an activity     |")
        print("| [2] Track your fitness  |")
        print("| [3] Plan your health    |")
        print(line)

        return username


"""This function checks if date is in the valid form MM/YYYY"""
def is_valid_date(date: str):
    # Check for use of correct separator '/'
    if "/" not in date:
        print("Please use '/' as a separator")
        return False

    else:
        # Split string to check validity of month and year separately
        month_year = date.split("/")

        month = month_year[0]
        year = month_year[1]

        if check_valid_month(month) and check_valid_year(year):
            return True

        else:
            return False


"""This function checks if date is in valid in MM format
where MM is less than equal to 12, and where any months less
than 10 have a leading zero."""

def check_valid_month(month):
    # Months must be at least two characters long
    if len(month) != 2:
        print("Please enter a valid month.")
        return False
    
    elif int(month[0]) == 1:
        if int(month[1]) > 2: 
            # Reject months greater than 12
            print("Please enter a valid month.")
            return False
        else: 
            return True

    elif int(month[0]) == 0:
        if int(month[1]) == 0:
            # Reject '00' as month
            print("Please enter a valid month.")
            return False
        else: 
            return True
            
    else: 
        # Any remaining dates from this point are invalid
        return False


"""This function checks if year YYYY is between 2000 and 2025."""
def check_valid_year(year):
    if 2000 <= int(year) <= 2025:
        return True
    else:
        print("Please enter a valid year.")
        return False


'''This function requests user data and stores it in a .txt file'''
def log_workout(username: str):
    exercise_type = input("What exercise would you like to log? ")

    # Convert input to lowercase for validation
    exercise = exercise_type.lower()

    # Reject invalid exercise names
    if (exercise != "swim") and (exercise != "run") and (exercise != "cycle"):
        print(f"Sorry, {exercise} is not supported.")
        return

    date = input(f"What month did you {exercise_type} (mm/yyyy)? ")
    # Check validity of date input
    if is_valid_date(date) == False:
        return

    distance_with_unit = input(f"What distance did you {exercise_type} (km or miles)? ")
    duration = input(f"How long did you {exercise_type} (minutes)? ")

    # Extract numerical part of distance input
    distance = str(extract_distance(distance_with_unit))

    filename = username + ".txt"  # Find file name from username
    user_data = f"""{exercise},{distance},{duration},{date}
"""
    # Append information to file
    f = open(filename, "a")
    f.write(user_data)
    f.close()


'''This function extracts numerical part of distance input
And converts kilometres if input is miles.'''
def extract_distance(distance_with_unit: str):
    # Split string to extract distance and unit separately
    split_distance = distance_with_unit.split()

    distance = float(split_distance[0])
    unit = split_distance[1]

    if unit == "miles":
        # Converting miles to kilometres
        distance = round(distance * 1.6, 1)
    else:
        distance = round(distance, 1)

    return distance


'''This function tracks the user's fitness and displays
a summary of their data.'''
def track_fitness(username):
    user = User(username)

    # Check if data exists
    if user.read_data() == False:
        return
    else:
        # Reject invalid exercise names
        exercise = input("What exercise would you like to track? ")
        if (exercise != "swim") and (exercise != "run") and (exercise != "cycle"):
            print(f"Sorry, {exercise} is not supported.")
            return

        month = input("What month would you like to track (mm/yyyy)? ")
        # If user requests all timeframes in given exercise
        if month == "all":
            month = None
        # Checking validity of month
        elif is_valid_date(month) == False:
            return

        # Count number of matching exercises by name and month
        # for average distance and duration calculation
        count = user.count_matching_data(exercise, month)

        total_distance = round(user.calculate_distance(exercise, month), 1)
        average_distance = round(total_distance / count, 1)
        total_duration = round(user.calculate_duration(exercise, month), 1)
        average_duration = int(round(total_duration / count, 0))
        # Converting from km per mins to km per hour
        average_speed = round((total_distance / total_duration) * 60, 2)
        average_speed_2dp = "{:.2f}".format(average_speed)

        print(f"Total distance: {total_distance}km")
        print(f"Average distance: {average_distance}km")
        print(f"Total duration: {total_duration} mins")
        print(f"Average duration: {average_duration} mins")
        print(f"Average speed (km/h): {average_speed_2dp}km/h")

    return


def health_plan(username):
    user = User(username)
    if user.read_data() == False:
        return

    else:
        goal_input = input("What goal would you like to achieve? ")
        goal = goal_input.lower()

        if (
            (goal != "marathon run")
            and (goal != "marathon swim")
            and (goal != "century")
            and (goal != "ironman")
            and (goal != "5 minute mile")
        ):
            print(f"Sorry, that goal is not supported.")
            return

        else:
            weeks = float(input("How many weeks do you have to achieve it? "))

        if goal == "marathon run":
            exercise_type = "run"
            goal_distance = 42
            print(f"To achieve the {goal_input} challenge you need to:")
            calculate_recommendation(
                user, exercise_type, goal_distance, goal_input, weeks
            )

        elif goal == "marathon swim":
            exercise_type = "swim"
            goal_distance = 10
            print(f"To achieve the {goal_input} challenge you need to:")
            calculate_recommendation(
                user, exercise_type, goal_distance, goal_input, weeks
            )

        elif goal == "century":
            exercise_type = "cycle"
            goal_distance = 100
            print(f"To achieve the {goal_input} challenge you need to:")
            calculate_recommendation(
                user, exercise_type, goal_distance, goal_input, weeks
            )

        elif goal == "ironman":
            # Each exercise in ironman has an associated distance value
            exercise_type = {"swim": 4, "cycle": 180, "run": 42}
            print(f"To achieve the {goal_input} challenge you need to:")
            for exercise in exercise_type:
                goal_distance = exercise_type[exercise]
                calculate_recommendation(
                    user, exercise, goal_distance, goal_input, weeks
                )

        elif goal == "5 minute mile":
            exercise_type = "run"
            goal_speed_km = 12 * 1.6
            max_speed = 0

            print(f"To achieve the {goal_input} challenge you need to:")

            for exercise in user.exercises:
                if exercise.name == exercise_type:
                    # Convert speed from miles per hour to kilometres per hour
                    speed_kilometres_hour = (exercise.distance / exercise.duration) * 60
                    # Determine maximum speed from exercises list of run type
                    if speed_kilometres_hour > max_speed:
                        max_speed = speed_kilometres_hour

            total_speed_needed = goal_speed_km - float(max_speed)

            if total_speed_needed <= 0:
                speed_per_week = 0.0
            else:
                speed_per_week = round(total_speed_needed / weeks, 2)

            print(f"    Increase your max speed by {speed_per_week}km/h per week.")


"""This function calculates the additional distance needed to reach goal."""
def calculate_recommendation(user, exercise_type, goal_distance, goal_input, weeks):
    maximum_distance = user.calculate_max_distance(exercise_type)

    total_distance_needed = goal_distance - float(maximum_distance)
    if total_distance_needed <= 0:
        distance_per_week = 0.0
    else:
        distance_per_week = round(total_distance_needed / weeks, 1)
        
    print(f"    Increase your max {exercise_type} by {distance_per_week}km per week.")


def main():
    # Print the welcome screen
    welcome_screen()

    # Ask the user to login with a username
    username = login()

    # If the username is too long, keep asking to login
    while username == None:
        username = login()
        if username != None:
            break

    option = input("Choose an option: ")
    if option == "1":
        log_workout(username)
    if option == "2":
        track_fitness(username)
    if option == "3":
        health_plan(username)
    return


if __name__ == "__main__":
    main()
