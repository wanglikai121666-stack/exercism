"""Functions to help Azara and Rui locate pirate treasure."""


def get_coordinate(record):
    return record[1]
    """Return coordinate value from a tuple containing the treasure name, and treasure coordinate.

    Parameters:
        record (tuple): A (treasure, coordinate) pair.

    Returns:
        str: The extracted map coordinate.
    """

    pass


def convert_coordinate(coordinate):
    return (coordinate[0],coordinate[1])
    """Split the given coordinate into tuple containing its individual components.

    Parameters:
        coordinate (str): A string map coordinate.

    Returns:
        tuple: The string coordinate split into its individual components.
    """

    pass


def compare_records(azara_record, rui_record):
    a=convert_coordinate(azara_record[1])
    return a==rui_record[1]
    """Compare two record types and determine if their coordinates match.

    Parameters:
        azara_record (tuple): A (treasure, coordinate) pair.
        rui_record (tuple): A (location, tuple(coordinate_1, coordinate_2), quadrant) trio.  
rui_record (元组): 一个 (位置, 元组(坐标 1, 坐标 2), 象限) 三元组。

    Returns:
        bool: Do the coordinates match?
    """

    pass


def create_record(azara_record, rui_record):
    if compare_records(azara_record, rui_record):
        return azara_record + rui_record
    return 'not a match'

        
    
    """Combine the two record types (if possible) and create a combined record group.

    Parameters:
        azara_record (tuple): A (treasure, coordinate) pair.
        rui_record (tuple): A (location, coordinate, quadrant) trio.  
rui_record (元组): 一个 (位置, 坐标, 象限) 的三元组。

    Returns:
        tuple or str: The combined record (if compatible), or the string "not a match" (if incompatible).
    """

    pass


def clean_up(combined_record_group):
    report = ""

    for combined_record in combined_record_group:
        cleaned_record = (
            combined_record[0],
            combined_record[2],
            combined_record[3],
            combined_record[4],
        )

        report += str(cleaned_record) + "\n"

    return report

    """Clean up a combined record group into a multi-line string of single records.

    Parameters:
        combined_record_group (tuple): Everything from both participants.

    Returns:
        str: Everything "cleaned", excess coordinates and information are removed.

    Note:
        The return statement is a multi-lined string with items separated by newlines.
        (see HINTS.md for an example).

    """

    pass
