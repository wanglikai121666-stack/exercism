class BowlingGame:
    def __init__(self):
        # 按顺序保存整局游戏的每次投球。
        # score() 最后会读取这个列表并计算总分。
        self.rolls = []

        # 当前正在进行的回合，从1开始。
        self.frame = 1

        # 保存当前回合已经投出的球。
        # 前9回合最多保存一球，因为第二球后立即结算；
        # 第10回合可能保存三球。
        self.current_frame = []

        # 标记游戏是否已经结束。
        self.game_over = False

    def roll(self, pins):
        """记录一次投球，并验证这次投球是否合法。"""

        # 游戏结束后不能继续投球。
        if self.game_over:
            raise ValueError("cannot roll after game is over")

        # 每次投球只能击倒0到10个球瓶。
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError("pins must be between 0 and 10")

        # 前9回合使用普通规则。
        if self.frame < 10:
            self._roll_normal_frame(pins)
            return

        # 第10回合使用特殊规则。
        self._roll_tenth_frame(pins)

    def _roll_normal_frame(self, pins):
        """处理第1到第9回合的投球。"""

        # current_frame为空，说明这是本回合第一球。
        if not self.current_frame:
            self.rolls.append(pins)

            # 第一球击倒10个，是Strike。
            # Strike一球就结束当前回合。
            if pins == 10:
                self.frame += 1
            else:
                # 不是Strike，需要等待本回合第二球。
                self.current_frame.append(pins)

            return

        # current_frame不为空，说明这是本回合第二球。
        first_roll = self.current_frame[0]

        # 同一回合的两球不能击倒超过10个球瓶。
        if first_roll + pins > 10:
            raise ValueError(
                "two rolls in a frame cannot exceed 10 pins"
            )

        # 记录第二球。
        self.rolls.append(pins)

        # 当前回合已经完成，清空临时记录。
        self.current_frame.clear()

        # 进入下一回合。
        self.frame += 1

    def _roll_tenth_frame(self, pins):
        """处理第10回合以及可能出现的奖励球。"""

        # 第10回合第一球。
        if not self.current_frame:
            self.rolls.append(pins)
            self.current_frame.append(pins)
            return

        # 第10回合第二球。
        if len(self.current_frame) == 1:
            first_roll = self.current_frame[0]

            # 如果第一球不是Strike，
            # 两球相加仍然不能超过10。
            if first_roll < 10 and first_roll + pins > 10:
                raise ValueError(
                    "two rolls in a frame cannot exceed 10 pins"
                )

            self.rolls.append(pins)
            self.current_frame.append(pins)

            # 第一球不是Strike，并且两球没有形成Spare，
            # 说明这是普通第10回合，没有奖励球。
            if first_roll < 10 and first_roll + pins < 10:
                self.game_over = True

            # 其他情况：
            # 第一球是Strike，需要第三球；
            # 或者两球构成Spare，也需要第三球。
            return

        # 能来到这里，说明正在投第10回合第三球。
        first_roll = self.current_frame[0]
        second_roll = self.current_frame[1]

        # 如果第10回合第一球是Strike，
        # 但第一颗奖励球不是Strike，
        # 那么两颗奖励球使用同一组10个球瓶。
        #
        # 例如：10、6、4 合法；
        #       10、6、5 非法。
        if (
            first_roll == 10
            and second_roll < 10
            and second_roll + pins > 10
        ):
            raise ValueError("invalid fill balls")

        # 记录第三球。
        self.rolls.append(pins)
        self.current_frame.append(pins)

        # 第10回合奖励球完成，整局结束。
        self.game_over = True

    def score(self):
        """游戏结束后计算10个回合的总分。"""

        # 游戏没有完成时不能计分。
        if not self.game_over:
            raise ValueError("cannot score an incomplete game")

        total = 0

        # 指向当前回合在self.rolls中的第一球。
        roll_index = 0

        # 一局固定计算10个回合。
        for _ in range(10):
            first_roll = self.rolls[roll_index]

            # Strike：
            # 当前10分，加后面两次投球。
            if first_roll == 10:
                strike_bonus = (
                    self.rolls[roll_index + 1]
                    + self.rolls[roll_index + 2]
                )

                total += 10 + strike_bonus

                # Strike只占用一条投球记录。
                roll_index += 1
                continue

            second_roll = self.rolls[roll_index + 1]

            # Spare：
            # 当前两球合计10分，加后面一次投球。
            if first_roll + second_roll == 10:
                spare_bonus = self.rolls[roll_index + 2]

                total += 10 + spare_bonus

                # Spare占用两条投球记录。
                roll_index += 2
                continue

            # 普通回合：
            # 没有奖励分，只计算当前两球。
            total += first_roll + second_roll

            # 普通回合占用两条投球记录。
            roll_index += 2

        return total