import math


def cipher_text(plain_text):
    normalized = ""

    for char in plain_text:
        if char.isalnum():
            normalized += char.lower()

    if normalized == "":
        return ""

    length = len(normalized)

    # 找到符合条件的列数 c 和行数 r
    # 条件：
    # r * c >= length
    # c >= r
    # c - r <= 1
    for c in range(1, length + 1):
        r = math.ceil(length / c)

        if r * c >= length and c >= r and c - r <= 1:
            break

    # 补空格，让文本刚好填满 r * c 的矩形
    normalized = normalized.ljust(r * c)

    # 按列读取
    chunks = []

    for col in range(c):
        chunk = ""

        for row in range(r):
            index = row * c + col
            chunk += normalized[index]

        chunks.append(chunk)

    return " ".join(chunks)