def get_positive_integer(message):
    while True:
        try:
            value = int(input(message))

            if value <= 0:
                print("Enter a value greater than 0.")
                continue

            return value

        except ValueError:
            print("Please enter a valid number.")


def get_non_negative_integer(message):
    while True:
        try:
            value = int(input(message))

            if value < 0:
                print("Enter 0 or a positive number.")
                continue

            return value

        except ValueError:
            print("Please enter a valid number.")


def get_positive_float(message):
    while True:
        try:
            value = float(input(message))

            if value <= 0:
                print("Enter a value greater than 0.")
                continue

            return value

        except ValueError:
            print("Please enter a valid number.")