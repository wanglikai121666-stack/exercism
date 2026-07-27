def can_chain(dominoes):
    """
    输入：
        [(2, 1), (2, 3), (1, 3)]

    可能输出：
        [(1, 2), (2, 3), (3, 1)]

    如果无法让全部骨牌组成闭环，返回 None。
    """

    # 空输入可以组成空链。
    if not dominoes:
        return []

    # degree：每个数字连接了几次。
    degree = {}

    # graph：某个数字能通过哪些骨牌连到其他数字。
    #
    # 例如骨牌 (1, 2) 的编号是 0：
    # graph[1] 会记住 0
    # graph[2] 也会记住 0
    graph = {}

    for index, (left, right) in enumerate(dominoes):
        # 统计两个端点的连接次数。
        degree[left] = degree.get(left, 0) + 1
        degree[right] = degree.get(right, 0) + 1

        # 为两个数字准备邻接骨牌列表。
        graph.setdefault(left, []).append(index)
        graph.setdefault(right, []).append(index)

    # ---------- 条件 1：每个数字的连接次数必须为偶数 ----------

    for number in degree:
        if degree[number] % 2 != 0:
            return None

    # ---------- 条件 2：所有数字必须连通 ----------

    start = dominoes[0][0]
    visited_numbers = set()
    stack = [start]

    while stack:
        current = stack.pop()

        if current in visited_numbers:
            continue

        visited_numbers.add(current)

        # 找到所有通过骨牌相连的数字。
        for domino_index in graph[current]:
            left, right = dominoes[domino_index]

            # current 是 left 时，邻居是 right；
            # current 是 right 时，邻居是 left。
            if current == left:
                neighbor = right
            else:
                neighbor = left

            if neighbor not in visited_numbers:
                stack.append(neighbor)

    # 有数字完全不连通，无法组成一条大环。
    if visited_numbers != set(degree):
        return None

    # ---------- 构造实际骨牌链：Hierholzer 算法 ----------

    # used 记录已经使用过的骨牌编号。
    # 即使出现重复骨牌，它们的 index 不同，仍会被当作不同骨牌。
    used = set()

    # stack 中保存：
    # (当前数字, 走到这个数字时所使用的骨牌方向)
    #
    # 第一项是起点，没有“进入它的骨牌”，所以是 None。
    stack = [(start, None)]

    # 回溯时收集到的骨牌顺序是反的。
    reversed_chain = []

    while stack:
        current, entered_domino = stack[-1]

        # 移除 graph[current] 中已经用过的骨牌编号。
        while graph[current] and graph[current][-1] in used:
            graph[current].pop()

        # current 已经没有可继续使用的骨牌。
        if not graph[current]:
            stack.pop()

            # 不是起点才有“进入当前节点的骨牌”。
            if entered_domino is not None:
                reversed_chain.append(entered_domino)

            continue

        # 取出一张还没使用的骨牌。
        domino_index = graph[current].pop()

        if domino_index in used:
            continue

        used.add(domino_index)

        left, right = dominoes[domino_index]

        # 根据当前所在数字，决定骨牌摆放方向。
        #
        # 当前在 left：
        # [left|right]，下一站是 right
        #
        # 当前在 right：
        # 把牌翻过来，变成 [right|left]，下一站是 left
        if current == left:
            oriented_domino = (left, right)
            next_number = right
        else:
            oriented_domino = (right, left)
            next_number = left

        # 沿着这张骨牌前进到下一个数字。
        stack.append((next_number, oriented_domino))

    # 回溯得到的是反向顺序，翻转后才是正确链条顺序。
    chain = list(reversed(reversed_chain))

    # 所有骨牌都应当恰好使用一次。
    if len(chain) != len(dominoes):
        return None

    return chain