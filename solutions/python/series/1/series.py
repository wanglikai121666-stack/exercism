def slices(series, length):
    if length == 0:
        raise ValueError("slice length cannot be zero")

    if length < 0:
        raise ValueError("slice length cannot be negative")

    if series == "":
        raise ValueError("series cannot be empty")

    if length > len(series):
        raise ValueError("slice length cannot be greater than series length")
    result = []
    max_start = len(series) - length
    for start in range(0, max_start + 1):
        end = start + length
        piece = series[start:end]
        result.append(piece)
    return result
