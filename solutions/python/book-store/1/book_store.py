from functools import lru_cache

# 全局常量
# 注意：Codewars 用 cents（美分，整数）作为价格单位，不用 dollars（美元，小数）
# 1 dollar = 100 cents
#   错误示例：total([2,2]) == 16 ❌（美元）→ 应该是 1600 ✅（cents）
#   错误示例：total([1,2]) == 15.20 ❌（美元）→ 应该是 1520 ✅（cents）
BOOK_PRICE = 800          # 每本书单价 800 cents = $8
# 折扣表：{组大小: 折扣率}
#   1 本 → 0%（不打折）
#   2 本不同 → 5%  off
#   3 本不同 → 10% off
#   4 本不同 → 20% off
#   5 本不同 → 25% off
DISCOUNT = {1: 0.0, 2: 0.05, 3: 0.10, 4: 0.20, 5: 0.25}


def total(basket):
    """
    计算购物篮中书籍的最低总价（最大化折扣）。

    问题描述：
      有一套 5 本书的系列，每本 $8 (800 cents)。
      购买多本不同书时享受折扣：
        2 本不同 → 5% off     (每本 760 cents)
        3 本不同 → 10% off    (每本 720 cents)
        4 本不同 → 20% off    (每本 640 cents)
        5 本不同 → 25% off    (每本 600 cents)
      注意：买 4 本书但只有 3 本不同时，仅对不同那 3 本打折，第 4 本原价。

      目标：将篮子里的书分成若干"组"，每组由不同书组成，使得总价最低。
      例如 basket=[0,0,1,1,2,2,3,4]（对应 2,2,2,1,1 份数）：
        - 分组 5+3 → 3000 + 2160 = 5160 cents
        - 分组 4+4 → 2560 + 2560 = 5120 cents ← 更优

    策略：
      用递归 + 记忆化搜索，尝试所有可能的分组方式。
      每次从剩余书中，尝试取 2~5 本不同的书组成一组。
      永远从"剩余最多"的书开始取（排序保证），这不会丢失最优解
      因为折扣只取决于"组里有几种不同的书"，不取决于具体是哪几本。

    参数：
      basket: list，每本书的 ID（一般是数字 0~4 或 1~5）

    返回值：
      int，最低总价，单位是 cents（整数）
    """
    # ---------- Step 1: 统计每种书的数量 ----------
    # 用 Counter 统计每种书出现了几次
    # 例如 basket=[0,0,1,1,2,2,3,4] →
    #   Counter({0:2, 1:2, 2:2, 3:1, 4:1})
    # 我们只需要"每种剩几本"的列表，不需要具体是哪种书
    # 因为 5 种书在计算折扣时是完全对称的
    from collections import Counter
    counter = Counter(basket)

    # 取出每种书的剩余数量，并从大到小排序
    # 例如 [2, 2, 2, 1, 1]
    # 排序是为了让同一状态（如 3 种书各剩 2 本、2 种书各剩 1 本）的
    # 表示唯一，方便记忆化缓存命中
    counts = sorted(counter.values(), reverse=True)

    # ---------- Step 2: 记忆化递归搜索最优价格 ----------
    @lru_cache(maxsize=None)
    def best_price(counts_tuple):
        """
        递归计算：给定剩余书的数量分布，最低总价是多少。

        参数 counts_tuple: 元组，按降序排列的剩余数量。
          例如 (2,2,2,1,1) 表示 8 本书剩着，其中：
            3 种书各剩 2 本
            2 种书各剩 1 本

        返回值: int，把这个状态买到最低需要多少钱（cents）
        """
        # 递归终止条件：没有书了，价格为 0
        if not counts_tuple:
            return 0

        # 转成 list 方便修改
        cnt = list(counts_tuple)

        # 当前还剩几种不同的书
        n = len(cnt)  # n ∈ [1, 5]

        # ---------- 尝试每种可能的分组大小 ----------
        # 从大到小尝试组大小（不一定最快但没区别，反正枚举全部）
        # 为什么不试 size=1？因为 1 本不打折，永远不会有优势
        # 它等价于把这个书留到别的组里。跳过 size=1 可以减少搜索空间。
        best = float('inf')

        # 尝试用 size 本不同书组成一组（size=2~n）
        for size in range(2, n + 1):
            # 从 cnt 里每种书各取 1 本，共取 size 本
            # 因为 cnt 已经排序过，取前 size 个数量最大的书
            new_cnt = []
            for i, c in enumerate(cnt):
                if i < size:
                    new_cnt.append(c - 1)  # 被取走 1 本
                else:
                    new_cnt.append(c)       # 没被取，数量不变

            # 去掉数量为 0 的书（后面的递归只会用到还有库存的书）
            new_cnt = [c for c in new_cnt if c > 0]
            # 再排序，保证状态表示唯一
            new_cnt.sort(reverse=True)

            # 计算：这组的价格 + 剩余书的最优价
            # 注意用 BOOK_PRICE=800 (cents)，所以最终结果自然是整数 cents
            group_price = size * BOOK_PRICE * (1 - DISCOUNT[size])
            total_price = group_price + best_price(tuple(new_cnt))

            # 保留更优的方案
            if total_price < best:
                best = total_price

        # ---------- 处理特殊情况 ----------
        # 如果上面循环没执行（说明 n=1，只剩 1 种书）
        # 那只能原价买，没有折扣
        if best == float('inf'):
            # n=1 时 cnt 只有 1 个元素
            # 例如 cnt=[5] 表示 5 本相同的书，全价 800×5=4000 cents
            best = cnt[0] * BOOK_PRICE

        return best

    # ---------- Step 3: 开始计算并返回 ----------
    # 传入初始状态的元组
    # 由于 BOOK_PRICE=800 且折扣率是 0.05 的整数倍，
    # 所有计算都是整数，没有浮点精度问题，直接返回 int
    return int(best_price(tuple(counts)))
