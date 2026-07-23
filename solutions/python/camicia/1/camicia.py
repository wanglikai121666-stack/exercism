from collections import deque


PAYMENT_CARDS = {
    "J": 1,
    "Q": 2,
    "K": 3,
    "A": 4,
}


def simulate_game(player_a, player_b):
    # 两位玩家的牌堆：左边是牌顶，右边是牌底。
    players = [
        deque(player_a),
        deque(player_b),
    ]

    # 本回合已经打出的中央牌堆。
    pile = deque()

    # 0 表示 A，1 表示 B。
    current = 0

    # 当前玩家还要支付多少张牌。
    # 0 表示没有正在生效的字母牌。
    penalty_due = 0

    cards = 0
    tricks = 0

    def collect_pile(winner):
        """winner 收走中央牌堆，并把牌放到自己牌堆底部。"""
        nonlocal tricks

        players[winner].extend(pile)
        pile.clear()
        tricks += 1

    def normalized_state():
        """
        用于循环检测。
        数字牌具体是什么不重要，统一变成 'N'；
        J/Q/K/A 必须保留。
        """
        return tuple(
            tuple(
                card if card in PAYMENT_CARDS else "N"
                for card in deck
            )
            for deck in players
        )

    # 初始状态也要记录。
    seen_states = {normalized_state()}

    while True:
        # 轮到 current 出牌，但他已经没有牌。
        if not players[current]:
            winner = 1 - current
            collect_pile(winner)

            return {
                "status": "finished",
                "cards": cards,
                "tricks": tricks,
            }

        # 从当前玩家的牌顶打出一张，放入中央牌堆。
        card = players[current].popleft()
        pile.append(card)
        cards += 1

        # 情况一：打出字母牌。
        if card in PAYMENT_CARDS:
            # 新字母牌会直接替换以前尚未完成的罚牌。
            penalty_due = PAYMENT_CARDS[card]

            # 对方开始支付。
            current = 1 - current
            continue

        # 情况二：打出数字牌，且目前正在支付罚牌。
        if penalty_due > 0:
            penalty_due -= 1

            # 还没支付完：同一个人继续出牌。
            if penalty_due > 0:
                continue

            # 已经支付完：
            # 当前玩家是支付者，所以对方（打出字母牌的人）收牌。
            winner = 1 - current
            collect_pile(winner)

            # 收牌后，如果有人没有牌，赢家拥有所有牌，游戏结束。
            if not players[0] or not players[1]:
                return {
                    "status": "finished",
                    "cards": cards,
                    "tricks": tricks,
                }

            # 收牌者开始下一回合。
            current = winner

            # 只在结算后、中央牌堆清空时检查循环。
            state = normalized_state()

            if state in seen_states:
                return {
                    "status": "loop",
                    "cards": cards,
                    "tricks": tricks,
                }

            seen_states.add(state)
            continue

        # 情况三：普通状态下打出数字牌，正常换人。
        current = 1 - current