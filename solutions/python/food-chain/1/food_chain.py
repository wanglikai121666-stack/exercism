def recite(start_verse, end_verse):
    # 按顺序保存 8 种动物
    animals = [
        "fly",
        "spider",
        "bird",
        "cat",
        "dog",
        "goat",
        "cow",
        "horse",
    ]

    # 每种动物对应的特殊句子
    reactions = [
        "",
        "It wriggled and jiggled and tickled inside her.",
        "How absurd to swallow a bird!",
        "Imagine that, to swallow a cat!",
        "What a hog, to swallow a dog!",
        "Just opened her throat and swallowed a goat!",
        "I don't know how she swallowed a cow!",
        "She's dead, of course!",
    ]

    # 最终要返回的所有歌词
    result = []

    # 从 start_verse 循环到 end_verse
    # end_verse + 1 是因为 range 不包含结束值
    for verse_number in range(start_verse, end_verse + 1):

        # 段数从 1 开始，列表下标从 0 开始
        index = verse_number - 1

        # 找到当前这一段的动物
        animal = animals[index]

        # 添加每一段固定的第一行
        result.append(
            f"I know an old lady who swallowed a {animal}."
        )

        # horse 是特殊情况
        if animal == "horse":

            # 添加 horse 的结尾
            result.append(reactions[index])

        else:
            # fly 没有特殊句子，所以要判断是否为空
            if reactions[index] != "":
                result.append(reactions[index])

            # 从当前动物向前倒着生成吞食链
            for current_index in range(index, 0, -1):

                # 当前动物
                current_animal = animals[current_index]

                # 当前动物前面的动物
                previous_animal = animals[current_index - 1]

                # 先生成普通的吞食句
                line = (
                    f"She swallowed the {current_animal} "
                    f"to catch the {previous_animal}"
                )

                # bird 抓 spider 时，需要添加蜘蛛的特殊描述
                if previous_animal == "spider":
                    line += (
                        " that wriggled and jiggled "
                        "and tickled inside her"
                    )

                # 在句子末尾添加句号
                line += "."

                # 把完整句子放进结果列表
                result.append(line)

            # 添加普通段落固定的苍蝇结尾
            result.append(
                "I don't know why she swallowed the fly. "
                "Perhaps she'll die."
            )

        # 如果当前不是最后一段，就添加一个空行
        if verse_number != end_verse:
            result.append("")

    # 返回所有歌词
    return result