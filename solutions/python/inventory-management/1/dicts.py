"""Functions to keep track and alter inventory."""


def create_inventory(items):
    report={}
    for number in items:
        if number in report:
            report[number] = report[number] + 1
        else:
            report[number] = 1 
    return report
def add_items(inventory, items):
    for number in items:
        if number in inventory:
            inventory[number]=inventory[number]+1
        else:
            inventory[number]=1
    return inventory
            
    """Add or increment items in inventory using elements from the items `list`.

    Parameters:
        inventory (dict): Dictionary of existing inventory.
        items (list): List of items to update the inventory with.

    Returns:
        dict: The inventory updated with the new items.
    """

    pass


def decrement_items(inventory, items):
    for number in items:
        if number in inventory and inventory[number]>=1 :
            inventory[number]=inventory[number]-1
    return inventory
    """Decrement items in inventory using elements from the `items` list.

    Parameters:
        inventory (dict): Inventory dictionary.
        items (list): List of items to decrement from the inventory.

    Returns:
        dict: Updated inventory with items decremented.
    """

    pass


def remove_item(inventory, item):
    if item in inventory :
            inventory.pop(item, None)
    return inventory
    """Remove item from inventory if it matches `item` string.

    Parameters:
        inventory (dict): Inventory dictionary.
        item (str): Item to remove from the inventory.

    Returns:
        dict: Updated inventory with item removed. Current inventory if item does not match.
    """

    pass


def list_inventory(inventory):
    output=[]
    for key in inventory:
        if inventory[key]>0:
            output.append((key,inventory[key]))
    return output
        
    """Create a list containing only available (item_name, item_count > 0) pairs in inventory.

    Parameters:
        inventory (dict): An inventory dictionary.

    Returns:
        list[tuple]: List of key, value tuples from the inventory dictionary.
    """

    pass
