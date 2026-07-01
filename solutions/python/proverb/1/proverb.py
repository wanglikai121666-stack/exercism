def proverb(*items, qualifier=None):
    lines = []
    
    if len(items) == 0:
        return lines
    for index in range(len(items) - 1):
        lines.append(
            f"For want of a {items[index]} the {items[index + 1]} was lost."
        )
    if len(items) > 0:
        first = items[0]
        if qualifier is not None:
            first = qualifier + " " + first
    lines.append(f"And all for the want of a {first}.")
    return lines
