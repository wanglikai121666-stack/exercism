from math import gcd


# 拉丁字母共有 26 个字母。
ALPHABET_SIZE = 26

# ord("a") 是字母 a 的 Unicode 编号。
# 后面会用它把 a～z 转换为 0～25。
FIRST_LETTER_CODE = ord("a")


def _validate_key(a):
    """
    检查 a 能不能作为合法密钥。

    gcd(a, 26) == 1 表示 a 和 26 互质，
    这种情况下才存在模逆，才可以正确解密。
    """
    if gcd(a, ALPHABET_SIZE) != 1:
        raise ValueError("a and m must be coprime.")


def _letter_to_number(letter):
    """
    把小写字母转换为 0～25 的编号。

    "a" -> 0
    "b" -> 1
    ...
    "z" -> 25
    """
    return ord(letter) - FIRST_LETTER_CODE


def _number_to_letter(number):
    """
    把编号转换回小写字母。

    % 26 保证结果始终在 0～25 的范围内，
    即使 number 是负数或大于 25 也没问题。
    """
    return chr((number % ALPHABET_SIZE) + FIRST_LETTER_CODE)


def _clean_text(text):
    """
    清洗输入文本：

    - 字母：转成小写并保留
    - 数字：原样保留
    - 空格、逗号、感叹号等标点：丢弃

    例如：
    "Testing, 123!"
    -> "testing123"
    """
    result = []

    for char in text.lower():
        # 只保留 a～z，避免其他语言字母也被当成英文处理。
        if "a" <= char <= "z":
            result.append(char)

        # 数字不需要加密，直接保留。
        elif char.isdigit():
            result.append(char)

    return "".join(result)


def _group_by_five(text):
    """
    把密文每 5 个字符分成一组。

    例如：
    "abcdefghijkl"
    -> "abcde fghij kl"

    注意：数字也算一个字符，也要参与每五个一组。
    """
    groups = []

    # range(0, len(text), 5) 的意思是：
    # 从 0 开始，每次向后跳 5 格。
    for start in range(0, len(text), 5):
        groups.append(text[start:start + 5])

    return " ".join(groups)


def encode(plain_text, a, b):
    """
    使用仿射密码加密 plain_text。

    加密公式：
    E(x) = (a * x + b) % 26
    """
    _validate_key(a)

    # 先删掉空格与标点，把字母统一变小写。
    cleaned_text = _clean_text(plain_text)

    encrypted_characters = []

    for char in cleaned_text:
        # 数字不加密，直接进入结果。
        if char.isdigit():
            encrypted_characters.append(char)
            continue

        # 1. 字母转编号，例如 "t" -> 19。
        original_number = _letter_to_number(char)

        # 2. 套用加密公式。
        encrypted_number = (
            a * original_number + b
        ) % ALPHABET_SIZE

        # 3. 新编号转回字母。
        encrypted_characters.append(
            _number_to_letter(encrypted_number)
        )

    # 先把单个字符合成连续密文，
    # 再按每五个字符插入一个空格。
    encrypted_text = "".join(encrypted_characters)
    return _group_by_five(encrypted_text)


def decode(ciphered_text, a, b):
    """
    使用仿射密码解密 ciphered_text。

    解密公式：
    D(y) = a 的模逆 * (y - b) % 26
    """
    _validate_key(a)

    # pow(a, -1, 26) 的意思：
    # 求 a 在“模 26”下的乘法逆元。
    #
    # 例如 a = 15 时：
    # 15 * 7 % 26 == 1
    # 所以 inverse_a == 7。
    inverse_a = pow(a, -1, ALPHABET_SIZE)

    # 解密同样忽略空格和标点。
    cleaned_text = _clean_text(ciphered_text)

    decrypted_characters = []

    for char in cleaned_text:
        # 数字原样保留。
        if char.isdigit():
            decrypted_characters.append(char)
            continue

        # 1. 密文字母转编号。
        encrypted_number = _letter_to_number(char)

        # 2. 套用解密公式。
        decrypted_number = (
            inverse_a * (encrypted_number - b)
        ) % ALPHABET_SIZE

        # 3. 编号转回原文字母。
        decrypted_characters.append(
            _number_to_letter(decrypted_number)
        )

    # 解密后的原文不需要每五个字符分组。
    return "".join(decrypted_characters)