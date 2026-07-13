def encode(message, rails):
    if rails <= 1 or rails >= len(message):
        return message

    # rails 行，len(message) 列
    fence = [
        [""] * len(message)
        for _ in range(rails)
    ]

    current_rail = 0
    direction = 1

    # 按之字形放入字符
    for column, character in enumerate(message):
        fence[current_rail][column] = character

        # 到达最上面，改为向下
        if current_rail == 0:
            direction = 1

        # 到达最下面，改为向上
        elif current_rail == rails - 1:
            direction = -1

        current_rail += direction

    result = []

    # 按行读取
    for row in fence:
        for character in row:
            if character != "":
                result.append(character)

    return "".join(result)


def decode(encoded_message, rails):
    if rails <= 1 or rails >= len(encoded_message):
        return encoded_message

    fence = [
        [""] * len(encoded_message)
        for _ in range(rails)
    ]

    current_rail = 0
    direction = 1

    # 第一步：标记之字形经过的位置
    for column in range(len(encoded_message)):
        fence[current_rail][column] = "?"

        if current_rail == 0:
            direction = 1
        elif current_rail == rails - 1:
            direction = -1

        current_rail += direction

    # 第二步：把密文按行填入标记位置
    message_index = 0

    for row in range(rails):
        for column in range(len(encoded_message)):
            if fence[row][column] == "?":
                fence[row][column] = encoded_message[message_index]
                message_index += 1

    # 第三步：沿着之字形路线读取
    result = []

    current_rail = 0
    direction = 1

    for column in range(len(encoded_message)):
        result.append(fence[current_rail][column])

        if current_rail == 0:
            direction = 1
        elif current_rail == rails - 1:
            direction = -1

        current_rail += direction

    return "".join(result)
