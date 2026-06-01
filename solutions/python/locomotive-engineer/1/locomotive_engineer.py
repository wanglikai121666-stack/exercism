"""Functions which helps the locomotive engineer to keep track of the train."""


def get_list_of_wagons(*args):
    return list(args)
    """Return a list of wagons, given an arbitrary amount of wagon numbers.

    Parameters:
        An arbitrary number of wagon numbers, unpacked.

    Returns:
        list: A list of wagon numbers.
    """
    pass


def fix_list_of_wagons(each_wagons_id, missing_wagons):
    first, second, locomotive, *rest = each_wagons_id
    return [locomotive, *missing_wagons, *rest, first, second]
    """Fix the list of wagons.

    Parameters:
        each_wagons_id (list[int]): The list of wagons.
        missing_wagons (list[int]): The list of missing wagons.

    Returns:
        list[int]: The corrected list of wagons.
    """
    pass


def add_missing_stops(route, **kwargs):
    list(kwargs.values())    
    return {**route, "stops": list(kwargs.values())}

#任意数量关键字参数 → **kwargs
#只要城市名 → kwargs.values()
#合并进原字典 → {**route, "stops": list(kwargs.values())}

    
    """Add missing stops to route dict.

    Parameters:
        route (dict): The dict of routing information.
        (dict): An arbitrary number of stops.

    Returns:
        dict: The updated route dictionary.
    """
    pass


def extend_route_information(route, more_route_information):
    return {**route, **more_route_information}
    """Extend route information with more_route_information.

    Parameters:
        route (dict): The route information.
        more_route_information (dict): The extra route information.

    Returns:
        dict: The extended route information.
    """
    pass


def fix_wagon_depot(wagons_rows):
    return [list(row) for row in zip(*wagons_rows)]

    """Fix the list of rows of wagons.

    Parameters:
        wagons_rows (list[list[tuple]]): The list of rows of wagons.

    Returns:
        list[list[tuple]]: the list of rows of wagons.
    """
    pass
