# 游戏的三种状态。
STATUS_WIN = "win"
STATUS_LOSE = "lose"
STATUS_ONGOING = "ongoing"


class Hangman:
    def __init__(self, word):
        # 保存玩家需要猜出的完整单词。
        #
        # 例如传入 "foobar" 后：
        # self.word == "foobar"
        self.word = word

        # 游戏开始时，玩家拥有 9 次剩余错误机会。
        self.remaining_guesses = 9

        # 新游戏的初始状态是“进行中”。
        self.status = STATUS_ONGOING

        # 使用集合记录玩家已经猜中的字母。
        #
        # 集合不会重复保存同一个字母。
        # 例如，连续添加两次 "b"，集合中仍然只有一个 "b"。
        self.guessed_letters = set()

    def guess(self, char):
        # 如果游戏已经获胜或失败，就不允许继续猜。
        #
        # 题目要求必须抛出 ValueError，
        # 并且异常中必须包含有意义的信息。
        if self.status != STATUS_ONGOING:
            raise ValueError("The game has already ended.")

        # 首先检查这个正确字母是否已经猜中过。
        #
        # 根据测试要求，即使这个字母存在于答案中，
        # 如果玩家重复猜它，也要扣除一次剩余机会。
        if char in self.guessed_letters:
            self.remaining_guesses -= 1

        # 如果这个字母没有猜过，并且存在于正确答案中，
        # 说明玩家进行了一次新的正确猜测。
        elif char in self.word:
            # 将正确字母加入已经猜中的字母集合。
            self.guessed_letters.add(char)

        else:
            # 如果字母不在正确答案中，说明玩家猜错了，
            # 因此扣除一次剩余机会。
            self.remaining_guesses -= 1

        # 将答案转换成集合，得到答案中所有不同的字母。
        #
        # 例如：
        # set("foobar") == {"f", "o", "b", "a", "r"}
        #
        # 虽然 "o" 在单词中出现了两次，
        # 但玩家只需要猜中一次字母 "o"。
        word_letters = set(self.word)

        # 如果答案中的所有不同字母都已经猜中，
        # 游戏状态就变成获胜。
        if word_letters == self.guessed_letters:
            self.status = STATUS_WIN

        # remaining_guesses 的初始值是 9。
        #
        # 第 9 次错误后：
        # remaining_guesses == 0
        #
        # 第 10 次错误后：
        # remaining_guesses == -1
        #
        # 根据测试要求，第 10 次错误后才判定失败。
        elif self.remaining_guesses < 0:
            self.status = STATUS_LOSE

        else:
            # 如果还没有猜出完整单词，
            # 并且错误机会还没有完全耗尽，
            # 游戏状态保持为“进行中”。
            self.status = STATUS_ONGOING

    def get_masked_word(self):
        # 创建一个列表，用来保存遮盖后的每一个字符。
        masked_characters = []

        # 按照原来的顺序遍历答案中的每个字母。
        for char in self.word:
            # 如果这个字母已经被玩家猜中，
            # 就显示正确的字母。
            if char in self.guessed_letters:
                masked_characters.append(char)

            else:
                # 如果这个字母还没有被玩家猜中，
                # 就使用下划线将它遮盖起来。
                masked_characters.append("_")

        # 把字符列表拼接成完整字符串。
        #
        # 例如：
        # ["_", "_", "_", "b", "_", "_"]
        #
        # 会被拼接成：
        # "___b__"
        return "".join(masked_characters)

    def get_status(self):
        # 返回当前游戏状态：
        #
        # STATUS_WIN
        # STATUS_LOSE
        # STATUS_ONGOING
        return self.status