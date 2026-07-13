from collections import deque


def find_fewest_coins(coins, target):
    if target < 0:
        raise ValueError("target can't be negative")

    if target == 0:
        return []

    # 队列中的每一项：
    # (当前已经凑出的金额, 当前使用的硬币组合)
    queue = deque([(0, [])])

    # 防止相同金额被重复搜索
    visited = {0}

    while queue:
        current_amount, used_coins = queue.popleft()#队列

        for coin in coins:
            next_amount = current_amount + coin

            # 超过目标，不需要继续
            if next_amount > target:
                continue

            next_coins = used_coins + [coin]

            # BFS 第一次到达目标，一定是硬币数量最少
            if next_amount == target:
                return sorted(next_coins)

            # 同一个金额只需要进入队列一次
            if next_amount not in visited:
                visited.add(next_amount)
                queue.append((next_amount, next_coins))

    raise ValueError("can't make target with given coins")