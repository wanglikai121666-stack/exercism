def encode(numbers):
    encoded = []

    for number in numbers:
        # 0 可以直接用一个字节表示
        if number == 0:
            encoded.append(0)
            continue

        groups = []

        # 每次取出最低 7 位
        while number > 0:
            groups.append(number & 0x7F)
            number >>= 7

        # 当前顺序是低位到高位，需要反转
        groups.reverse()

        # 除最后一组外，其他组的最高位设为 1
        for index in range(len(groups) - 1):
            groups[index] |= 0x80

        encoded.extend(groups)

    return encoded


def decode(bytes_):
    decoded = []
    value = 0
    incomplete = False

    for byte in bytes_:
        # 把旧数据左移 7 位，再拼上当前字节的低 7 位
        value = (value << 7) | (byte & 0x7F)

        # 最高位是 1，说明当前数字还没结束
        if byte & 0x80:
            incomplete = True

        # 最高位是 0，说明当前数字结束
        else:
            decoded.append(value)
            value = 0
            incomplete = False

    # 字节读完了，但最后一个数字仍未结束
    if incomplete:
        raise ValueError("incomplete sequence")

    return decoded