from collections import deque
from math import gcd


def measure(bucket_one, bucket_two, goal, start_bucket):
    """
    输入示例：
        measure(2, 3, 3, "one")

    输出示例：
        (2, "two", 2)

    含义：
        需要 2 步；
        桶二装着目标水量 3L；
        桶一还剩 2L。
    """

    # ---------- 1. 先判断目标是否有可能量出 ----------

    # 目标不能超过任一桶的最大容量。
    if goal > max(bucket_one, bucket_two):
        raise ValueError("Goal is larger than both buckets.")

    # 目标必须是两个容量最大公约数的倍数。
    # 否则无论怎样装、倒、互倒，都无法得到目标水量。
    if goal % gcd(bucket_one, bucket_two) != 0:
        raise ValueError("Goal cannot be measured with these bucket sizes.")

    # ---------- 2. 第一步必须装满指定的起始桶 ----------

    if start_bucket == "one":
        # 第一步：装满桶一
        first_state = (bucket_one, 0)

        # 禁止状态：起始桶一空，桶二满
        forbidden_state = (0, bucket_two)

    elif start_bucket == "two":
        # 第一步：装满桶二
        first_state = (0, bucket_two)

        # 禁止状态：起始桶二空，桶一满
        forbidden_state = (bucket_one, 0)

    else:
        raise ValueError("start_bucket must be 'one' or 'two'.")

    # queue 内每个元素的格式：
    #
    # (
    #     桶一当前水量,
    #     桶二当前水量,
    #     已操作步数
    # )
    #
    # 第一步已经装满了起始桶，因此步数从 1 开始。
    queue = deque([
        (first_state[0], first_state[1], 1)
    ])

    # 记录访问过的状态，避免来回倒水造成无限循环。
    visited = {first_state}

    # ---------- 3. BFS：每次从当前状态尝试全部合法操作 ----------

    while queue:
        one_current, two_current, moves = queue.popleft()

        # 任一桶达到目标，直接返回。
        # BFS 第一次找到目标时，一定是最少步数。
        if one_current == goal:
            return (moves, "one", two_current)

        if two_current == goal:
            return (moves, "two", one_current)

        # 保存“从当前状态做一次操作”后得到的所有状态。
        next_states = []

        # 操作 1：装满桶一
        next_states.append((bucket_one, two_current))

        # 操作 2：装满桶二
        next_states.append((one_current, bucket_two))

        # 操作 3：倒空桶一
        next_states.append((0, two_current))

        # 操作 4：倒空桶二
        next_states.append((one_current, 0))

        # 操作 5：桶一倒入桶二。
        #
        # 一次倒到：
        # - 桶一空，或
        # - 桶二满。
        one_to_two = min(
            one_current,
            bucket_two - two_current,
        )

        next_states.append((
            one_current - one_to_two,
            two_current + one_to_two,
        ))

        # 操作 6：桶二倒入桶一。
        two_to_one = min(
            two_current,
            bucket_one - one_current,
        )

        next_states.append((
            one_current + two_to_one,
            two_current - two_to_one,
        ))

        # 检查每一种下一步操作。
        for next_one, next_two in next_states:
            next_state = (next_one, next_two)

            # 例如桶一已经满，仍然执行“装满桶一”，
            # 水量没有变化，不应视为一次有效操作。
            if next_state == (one_current, two_current):
                continue

            # 排除题目明确禁止的状态。
            if next_state == forbidden_state:
                continue

            # 已经到过的状态不用再次搜索。
            if next_state in visited:
                continue

            visited.add(next_state)

            # 从当前状态走到下一状态，操作次数加一。
            queue.append((
                next_one,
                next_two,
                moves + 1,
            ))

    # 前面的 gcd 判断一般已排除这种情况；
    # 这里作为兜底。
    raise ValueError("Goal cannot be measured with these bucket sizes.")