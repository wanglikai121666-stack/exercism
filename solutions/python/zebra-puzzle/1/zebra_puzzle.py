from itertools import permutations


# 五栋房子在程序中使用 0～4 表示。
# 也就是：
# 0 = 第1栋
# 1 = 第2栋
# 2 = 第3栋
# 3 = 第4栋
# 4 = 第5栋
HOUSES = range(5)


def _put(slots, position, value):
    """
    尝试把 value 放到 slots 的指定位置。

    如果该位置为空，放入并返回 True。
    如果该位置已经是同一个值，也返回 True。
    如果该位置已经被另一个值占据，说明规则冲突，返回 False。
    """
    if slots[position] is None:
        slots[position] = value
        return True

    return slots[position] == value


def _neighbors(position):
    """
    返回某栋房子的所有邻居位置。

    第1栋只有第2栋一个邻居；
    第5栋只有第4栋一个邻居；
    中间房子有左右两个邻居。
    """
    result = []

    if position - 1 >= 0:
        result.append(position - 1)

    if position + 1 < 5:
        result.append(position + 1)

    return result


def _solve():
    """
    求出斑马谜题的唯一解。

    返回一个字典：
    {
        "water": 喝水者的国籍,
        "zebra": 斑马主人的国籍,
    }
    """

    # ---------------------------------------------------------
    # 第一层：颜色
    # ---------------------------------------------------------
    #
    # 挪威人住第1栋，挪威人隔壁是蓝房。
    # 所以蓝房只能在第2栋，也就是索引 1。
    blue_position = 1

    # 绿房必须紧挨着在象牙房的右边。
    #
    # 因为第2栋已经是蓝房，所以“象牙房、绿房”只能是：
    #
    # 第3栋、第4栋  -> 索引 2、3
    # 第4栋、第5栋  -> 索引 3、4
    #
    # 不需要枚举全部 5! 种颜色排列。
    possible_ivory_positions = [2, 3]

    for ivory_position in possible_ivory_positions:
        green_position = ivory_position + 1

        colors = [None] * 5
        colors[blue_position] = "blue"
        colors[ivory_position] = "ivory"
        colors[green_position] = "green"

        # 剩余的两个位置放红房和黄房。
        remaining_color_positions = [
            position
            for position in HOUSES
            if colors[position] is None
        ]

        for red_position, yellow_position in permutations(
            remaining_color_positions
        ):
            current_colors = colors.copy()
            current_colors[red_position] = "red"
            current_colors[yellow_position] = "yellow"

            # -------------------------------------------------
            # 第二层：国籍
            # -------------------------------------------------
            #
            # 挪威人固定住第1栋。
            norwegian_position = 0

            # 英国人住在红房，所以英国人的位置就是红房位置。
            englishman_position = red_position

            # 如果红房恰好在第1栋，就会要求：
            #
            # 第1栋同时住挪威人和英国人
            #
            # 这是不可能的，立即剪枝。
            if englishman_position == norwegian_position:
                continue

            nationalities = [None] * 5
            nationalities[norwegian_position] = "Norwegian"
            nationalities[englishman_position] = "Englishman"

            remaining_nationality_positions = [
                position
                for position in HOUSES
                if nationalities[position] is None
            ]

            remaining_nationalities = [
                "Spaniard",
                "Ukrainian",
                "Japanese",
            ]

            # 只需要枚举剩下三个人：
            # 3! = 6 种情况。
            for nationality_order in permutations(
                remaining_nationalities
            ):
                current_nationalities = nationalities.copy()

                for position, nationality in zip(
                    remaining_nationality_positions,
                    nationality_order,
                ):
                    current_nationalities[position] = nationality

                ukrainian_position = current_nationalities.index(
                    "Ukrainian"
                )
                japanese_position = current_nationalities.index(
                    "Japanese"
                )
                spaniard_position = current_nationalities.index(
                    "Spaniard"
                )

                # ---------------------------------------------
                # 第三层：饮料
                # ---------------------------------------------
                drinks = [None] * 5

                # 中间的第3栋喝牛奶。
                if not _put(drinks, 2, "milk"):
                    continue

                # 绿房主人喝咖啡。
                if not _put(
                    drinks,
                    green_position,
                    "coffee",
                ):
                    continue

                # 乌克兰人喝茶。
                if not _put(
                    drinks,
                    ukrainian_position,
                    "tea",
                ):
                    continue

                # 如果上面三条规则没有冲突，
                # 只剩水和橙汁需要安排。
                remaining_drink_positions = [
                    position
                    for position in HOUSES
                    if drinks[position] is None
                ]

                # 正常情况下应该刚好剩两个位置。
                if len(remaining_drink_positions) != 2:
                    continue

                for remaining_drinks in permutations(
                    ["water", "orange juice"]
                ):
                    current_drinks = drinks.copy()

                    for position, drink in zip(
                        remaining_drink_positions,
                        remaining_drinks,
                    ):
                        current_drinks[position] = drink

                    orange_juice_position = current_drinks.index(
                        "orange juice"
                    )
                    water_position = current_drinks.index("water")

                    # -----------------------------------------
                    # 第四层：爱好
                    # -----------------------------------------
                    hobbies = [None] * 5

                    # 黄房主人是画家。
                    if not _put(
                        hobbies,
                        yellow_position,
                        "painting",
                    ):
                        continue

                    # 日本人下棋。
                    if not _put(
                        hobbies,
                        japanese_position,
                        "chess",
                    ):
                        continue

                    # 踢足球的人喝橙汁。
                    if not _put(
                        hobbies,
                        orange_juice_position,
                        "football",
                    ):
                        continue

                    # 剩下的爱好只有跳舞和阅读。
                    remaining_hobby_positions = [
                        position
                        for position in HOUSES
                        if hobbies[position] is None
                    ]

                    if len(remaining_hobby_positions) != 2:
                        continue

                    for remaining_hobbies in permutations(
                        ["dancing", "reading"]
                    ):
                        current_hobbies = hobbies.copy()

                        for position, hobby in zip(
                            remaining_hobby_positions,
                            remaining_hobbies,
                        ):
                            current_hobbies[position] = hobby

                        dancing_position = current_hobbies.index(
                            "dancing"
                        )
                        reading_position = current_hobbies.index(
                            "reading"
                        )
                        painter_position = current_hobbies.index(
                            "painting"
                        )

                        # -------------------------------------
                        # 第五层：宠物
                        # -------------------------------------
                        pets = [None] * 5

                        # 西班牙人养狗。
                        if not _put(
                            pets,
                            spaniard_position,
                            "dog",
                        ):
                            continue

                        # 喜欢跳舞的人养蜗牛。
                        if not _put(
                            pets,
                            dancing_position,
                            "snails",
                        ):
                            continue

                        # 阅读者住在狐狸主人隔壁。
                        #
                        # 狐狸只需要尝试阅读者的邻居，
                        # 不需要尝试全部五栋房。
                        for fox_position in _neighbors(
                            reading_position
                        ):
                            pets_with_fox = pets.copy()

                            if not _put(
                                pets_with_fox,
                                fox_position,
                                "fox",
                            ):
                                continue

                            # 画家的房子在养马者隔壁。
                            #
                            # 马同样只尝试画家的邻居。
                            for horse_position in _neighbors(
                                painter_position
                            ):
                                final_pets = pets_with_fox.copy()

                                if not _put(
                                    final_pets,
                                    horse_position,
                                    "horse",
                                ):
                                    continue

                                # 狗、蜗牛、狐狸、马已经放好后，
                                # 剩下的唯一空位就是斑马的位置。
                                empty_positions = [
                                    position
                                    for position in HOUSES
                                    if final_pets[position] is None
                                ]

                                if len(empty_positions) != 1:
                                    continue

                                zebra_position = empty_positions[0]
                                final_pets[zebra_position] = "zebra"

                                # 找到完整合法方案后，
                                # 根据房子位置查询对应国籍。
                                return {
                                    "water": current_nationalities[
                                        water_position
                                    ],
                                    "zebra": current_nationalities[
                                        zebra_position
                                    ],
                                }

    # 如果所有可能性都检查完仍然没有结果，
    # 说明规则或代码存在矛盾。
    raise ValueError("No solution found")


# 只求解一次，两个公开函数直接读取结果。
SOLUTION = _solve()


def drinks_water():
    # 返回喝水者的国籍
    return SOLUTION["water"]


def owns_zebra():
    # 返回斑马主人的国籍
    return SOLUTION["zebra"]