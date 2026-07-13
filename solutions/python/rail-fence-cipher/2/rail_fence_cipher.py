def get_rail_pattern(length, rails):
    pattern = []

    current_rail = 0
    direction = 1

    for _ in range(length):
        pattern.append(current_rail)

        if current_rail == 0:
            direction = 1
        elif current_rail == rails - 1:
            direction = -1

        current_rail += direction

    return pattern


def encode(message, rails):
    if rails <= 1 or rails >= len(message):
        return message

    pattern = get_rail_pattern(len(message), rails)

    rail_contents = [[] for _ in range(rails)]

    for character, rail_number in zip(message, pattern):
        rail_contents[rail_number].append(character)

    result = []

    for rail in rail_contents:
        result.extend(rail)

    return "".join(result)


def decode(encoded_message, rails):
    if rails <= 1 or rails >= len(encoded_message):
        return encoded_message

    # 原文字符原本经过哪些轨道
    pattern = get_rail_pattern(len(encoded_message), rails)

    # 统计每条轨道需要多少字符
    rail_counts = [0] * rails

    for rail_number in pattern:
        rail_counts[rail_number] += 1

    # 把密文按轨道切开
    rail_contents = []
    start = 0

    for count in rail_counts:
        end = start + count
        rail_contents.append(encoded_message[start:end])
        start = end

    # 记录每条轨道已经读取到哪个位置
    rail_positions = [0] * rails

    result = []

    # 按原来的之字形顺序读取
    for rail_number in pattern:
        position = rail_positions[rail_number]

        character = rail_contents[rail_number][position]
        result.append(character)

        rail_positions[rail_number] += 1

    return "".join(result)