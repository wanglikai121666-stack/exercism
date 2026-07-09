RANK_VALUE = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


def best_hands(hands):
    """
    从 hands 里面找出最强的手牌。
    如果有多个并列最强，就全部返回。
    """
    best_score = None
    winners = []

    for hand in hands:
        score = score_hand(hand)

        if best_score is None:
            best_score = score
            winners = [hand]
        elif score > best_score:
            best_score = score
            winners = [hand]
        elif score == best_score:
            winners.append(hand)

    return winners


def score_hand(hand):
    """
    给一手牌打分。

    score 格式：
    (牌型等级, 同牌型内部比较列表)

    例如：
    (8, [14]) 表示 A 高同花顺
    (1, [13, 10, 8, 3]) 表示一对 K，散牌 10、8、3
    """
    ranks, suits = parse_hand(hand)

    counts = count_ranks(ranks)

    # 只看点数出现次数的结构
    # [4, 1]       = 四条
    # [3, 2]       = 葫芦
    # [3, 1, 1]    = 三条
    # [2, 2, 1]    = 两对
    # [2, 1, 1, 1] = 一对
    count_pattern = sorted(counts.values(), reverse=True)

    # 同花：所有花色都一样
    is_flush = len(set(suits)) == 1

    # 顺子：点数连续
    is_straight, straight_high = check_straight(ranks)

    # 8. 同花顺：既是顺子，又是同花
    if is_straight and is_flush:
        return (8, [straight_high])

    # 7. 四条：四张同点数 + 一张散牌
    if count_pattern == [4, 1]:
        four_rank = get_ranks_by_count(counts, 4)[0]
        kicker = get_ranks_by_count(counts, 1)[0]
        return (7, [four_rank, kicker])

    # 6. 葫芦：三条 + 一对
    if count_pattern == [3, 2]:
        three_rank = get_ranks_by_count(counts, 3)[0]
        pair_rank = get_ranks_by_count(counts, 2)[0]
        return (6, [three_rank, pair_rank])

    # 5. 同花：花色全一样，内部按点数从大到小比
    if is_flush:
        return (5, sorted(ranks, reverse=True))

    # 4. 顺子：内部只比最高牌
    if is_straight:
        return (4, [straight_high])

    # 3. 三条：三张同点数 + 两张散牌
    if count_pattern == [3, 1, 1]:
        three_rank = get_ranks_by_count(counts, 3)[0]
        kickers = get_ranks_by_count(counts, 1)
        return (3, [three_rank] + kickers)

    # 2. 两对：两个对子 + 一张散牌
    if count_pattern == [2, 2, 1]:
        pairs = get_ranks_by_count(counts, 2)
        kicker = get_ranks_by_count(counts, 1)[0]
        return (2, pairs + [kicker])

    # 1. 一对：一个对子 + 三张散牌
    if count_pattern == [2, 1, 1, 1]:
        pair_rank = get_ranks_by_count(counts, 2)[0]
        kickers = get_ranks_by_count(counts, 1)
        return (1, [pair_rank] + kickers)

    # 0. 高牌：什么特殊牌型都没有
    return (0, sorted(ranks, reverse=True))


def parse_hand(hand):
    """
    把一手牌拆成点数列表和花色列表。

    例如：
    "4S 10H AD 3C KS"

    拆成：
    ranks = [4, 10, 14, 3, 13]
    suits = ["S", "H", "D", "C", "S"]
    """
    cards = hand.split()

    ranks = []
    suits = []

    for card in cards:
        suit = card[-1]
        rank = card[:-1]

        ranks.append(RANK_VALUE[rank])
        suits.append(suit)

    return ranks, suits


def count_ranks(ranks):
    """
    用字典统计每个点数出现几次。
    """
    counts = {}

    for rank in ranks:
        if rank not in counts:
            counts[rank] = 0

        counts[rank] += 1

    return counts


def check_straight(ranks):
    """
    判断是不是顺子。

    返回：
    (True, 最高牌) 或 (False, None)
    """
    unique_ranks = sorted(set(ranks))

    # A 2 3 4 5 是特殊顺子，最高牌按 5 算
    if unique_ranks == [2, 3, 4, 5, 14]:
        return True, 5

    # 普通顺子：5 个不同点数，并且最大值 - 最小值 = 4
    if len(unique_ranks) == 5 and unique_ranks[-1] - unique_ranks[0] == 4:
        return True, unique_ranks[-1]

    return False, None


def get_ranks_by_count(counts, target_count):
    """
    从 counts 字典里找出“出现次数等于 target_count”的点数。

    例如：
    counts = {13: 2, 10: 1, 8: 1, 3: 1}

    get_ranks_by_count(counts, 2) -> [13]
    get_ranks_by_count(counts, 1) -> [10, 8, 3]
    """
    result = []

    for rank, count in counts.items():
        if count == target_count:
            result.append(rank)

    return sorted(result, reverse=True)