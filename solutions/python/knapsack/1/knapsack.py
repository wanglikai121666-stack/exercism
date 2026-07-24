def maximum_value(maximum_weight, items):
    best_value = 0
    item_count = len(items)

    # 2 ** item_count 表示所有可能的组合数量。
    for mask in range(2 ** item_count):
        total_weight = 0
        total_value = 0

        # 检查当前组合选择了哪些物品。
        for index in range(item_count):
            # 判断二进制的第index位是否为1。
            if mask & (1 << index):
                total_weight += items[index]["weight"]
                total_value += items[index]["value"]

        # 当前组合没有超重，才有资格更新最大价值。
        if total_weight <= maximum_weight:
            best_value = max(best_value, total_value)

    return best_value