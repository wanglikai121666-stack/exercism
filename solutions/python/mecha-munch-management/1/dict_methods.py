"""Functions to manage a users shopping cart items."""


def add_item(current_cart, items_to_add):
    for item in items_to_add :
        if item in current_cart:
            current_cart[item]=current_cart[item]+1
        else :
            current_cart[item]=1
    return current_cart
            
            
            
    
    """Add items to shopping cart.

    Parameters:
        current_cart (dict): The current shopping cart.
        items_to_add (iterable): The items to add to the cart.

    Returns:
        dict: The updated user cart dictionary.
    """

    pass


def read_notes(notes):
    return dict.fromkeys(notes,1)
    """Create user cart from an iterable notes entry.

    Parameters:
        notes (iterable): Group of items to add to cart.

    Returns:
        dict: A user shopping cart dictionary.
    """

    pass


def update_recipes(ideas, recipe_updates):
    ideas.update(recipe_updates)
    return ideas
    """Update the recipe ideas dictionary.

    Parameters:
        ideas (dict): The "recipe ideas" dict.
        recipe_updates (iterable): Updates for the ideas section.

    Returns:
        dict: The updated "recipe ideas" dict.
    """

    pass


def sort_entries(cart):
    return dict(sorted(cart.items()))
    """Sort a user's shopping cart in alphabetical order.

    Parameters:
        cart (dict): A user's shopping cart dictionary.

    Returns:
        dict: A user's shopping cart sorted in alphabetical order.
    """

    pass


def send_to_store(cart, aisle_mapping):
    fulfillment_cart = {}
    sorted_cart_items = sorted(cart.items(), reverse=True)
    for cart_item in sorted_cart_items:
        item_name = cart_item[0]
        item_quantity = cart_item[1]
        aisle_info = aisle_mapping[item_name]
        aisle_name = aisle_info[0]
        needs_refrigeration = aisle_info[1]
        fulfillment_cart[item_name]= [
            item_quantity,
            aisle_name,
            needs_refrigeration,                    #先洗数据然后统一拼接组合的思路
        ]
    return fulfillment_cart
                
            
    """Combine user's order to aisle and refrigeration information.

    Parameters:
        cart (dict): The user's shopping cart dictionary.
        aisle_mapping (dict): The aisle and refrigeration information dictionary.

    Returns:
        dict: The fulfillment dictionary ready to send to store.
    """

    pass


def update_store_inventory(fulfillment_cart, store_inventory):
    for item, order_info in fulfillment_cart.items():
        ordered_quantity = order_info[0]
        store_inventory[item][0] -= ordered_quantity
        if store_inventory[item][0] <= 0:
            store_inventory[item][0] = "Out of Stock"
    return store_inventory
    
    """Update store inventory levels with user order.

    Parameters:
        fulfillment cart (dict): The fulfillment cart to send to store.
        store_inventory (dict): The stores available inventory.

    Returns:
        dict: The store_inventory updated.
    """

    pass
