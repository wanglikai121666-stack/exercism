from itertools import permutations


def solve(puzzle):
    # 例如：
    # "SEND + MORE == MONEY"
    # 左边：["SEND", "MORE"]
    # 右边："MONEY"
    left_side, right_word = puzzle.split(" == ")
    left_words = left_side.split(" + ")

    # 把左右两边所有单词放在一起，后面统一处理
    all_words = left_words + [right_word]

    # 收集所有不同字母。
    # set 会自动去重，例如 SEND 中重复出现的字母只保留一次。
    letters = set("".join(all_words))

    # 一个字母必须对应一个不同数字。
    # 但数字只有 0 到 9，所以超过 10 个字母一定无解。
    if len(letters) > 10:
        return None

    # 多位数的第一个字母不能是 0。
    # 例如 SEND 不能被转换成 0567。
    leading_letters = {
        word[0]
        for word in all_words
        if len(word) > 1
    }

    # 尝试把不同的数字分配给不同的字母。
    # 例如 letters 有 3 个字母，就从 0~9 中取 3 个不重复数字。
    for digits in permutations(range(10), len(letters)):

        # 例如：
        # letters = {"I", "B", "L"}
        # digits = (1, 9, 0)
        # 得到 {"I": 1, "B": 9, "L": 0}
        mapping = dict(zip(letters, digits))

        # 如果任何多位数的首字母被分配到 0，这种方案无效。
        if any(mapping[letter] == 0 for letter in leading_letters):
            continue

        # 把一个字母单词转换成真正的整数。
        # 例如 mapping 中 S=9、E=5、N=6、D=7：
        # "SEND" -> "9567" -> 9567
        def word_to_number(word):
            number_text = ""

            for letter in word:
                number_text += str(mapping[letter])

            return int(number_text)

        # 左边所有单词分别转换成数字后相加。
        # SEND + MORE -> 9567 + 1085
        left_sum = sum(word_to_number(word) for word in left_words)

        # 右边单词转换成数字。
        # MONEY -> 10652
        right_sum = word_to_number(right_word)

        # 当前数字分配能让等式成立，就是答案。
        if left_sum == right_sum:
            return mapping

    # 尝试完所有分配方式仍不成立，表示无解。
    return None