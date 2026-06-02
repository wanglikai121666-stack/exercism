"""Functions to automate Conda airlines ticketing system."""


def generate_seat_letters(number):
    seat_letters ="ABCD"
    for index in range(number):
        yield seat_letters[index % 4]
    """Generate a series of letters for airline seats.

    Parameters:
        number (int): Total number of seat letters to be generated.

    Returns:
        generator: A generator that yields seat letters.

    Note:
        Seat letters are generated from A to D.
        After D the sequence starts again with A.
        For example: A, B, C, D, A, B

    """

    pass


def generate_seats(number):
    row=1
    seat_count_in_row = 0

    for letter in generate_seat_letters(number):
        if row==13:
            row+=1
        yield f"{row}{letter}"
        seat_count_in_row += 1
        if seat_count_in_row == 4:
            row+=1
            seat_count_in_row = 0
        
    """Generate a series of identifiers for airline seats.

    Parameters:
        number (int): The total number of seats to be generated.

    Returns:
        generator: A generator that yields seat numbers.

    Note:
        A seat number consists of the row number and the seat letter.
        There is no row 13, and each row has 4 seats.

        Seats should be sorted from low to high.
        For example: 3C, 3D, 4A, 4B

    """

    pass


def assign_seats(passengers):
    seats = generate_seats(len(passengers))
    assigned_seats = {}
    for passenger in passengers:
        assigned_seats[passenger] = next(seats)
    return assigned_seats
    """Assign seats to passengers.

    Parameters:
        passengers (list[str]): A list of strings containing names of passengers.

    Returns:
        dict: With passenger names as keys and seat numbers as values.
        Example output: {"Adele": "1A", "Björk": "1B"}

    """

    pass


def generate_codes(seat_numbers, flight_id):
    for seat_number in seat_numbers:
        temple=f"{seat_number}{flight_id}"
        zeros_needed = 12 - len(temple)
        yield temple + "0" * zeros_needed
            
    """Generate codes for a ticket.

    Parameters:
        seat_numbers (list[str]): A list of seat numbers.
        flight_id (str): A string containing the flight identifier.

    Returns:
        generator: A generator that yields 12 character long ticket codes.

    """

    pass
