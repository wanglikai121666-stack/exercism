def grep(pattern, flags, files):
    # 保存最终输出的所有匹配结果
    results = []

    # flags 是字符串，例如：
    # "-n"
    # "-n -i"
    #
    # split() 将它拆成：
    # ["-n"]
    # ["-n", "-i"]
    flag_set = set(flags.split())

    # 搜索多个文件时，需要在匹配行前显示文件名
    multiple_files = len(files) > 1

    # 依次处理每一个文件
    for file_name in files:
        # 打开当前文件；离开 with 后自动关闭
        with open(file_name, encoding="utf-8") as file:
            # enumerate(..., start=1) 让行号从 1 开始
            for line_number, raw_line in enumerate(file, start=1):
                # 去掉行末换行符，方便比较和格式化
                line = raw_line.rstrip("\n")

                # 准备实际用于比较的文本
                compared_line = line
                compared_pattern = pattern

                # -i：忽略大小写
                if "-i" in flag_set:
                    compared_line = compared_line.casefold()
                    compared_pattern = compared_pattern.casefold()

                # -x：要求整行完全相等
                if "-x" in flag_set:
                    is_match = compared_line == compared_pattern
                else:
                    # 默认：只要当前行包含搜索字符串即可
                    is_match = compared_pattern in compared_line

                # -v：反转匹配结果
                if "-v" in flag_set:
                    is_match = not is_match

                # 当前行不符合条件，检查下一行
                if not is_match:
                    continue

                # -l：只输出包含匹配结果的文件名
                if "-l" in flag_set:
                    results.append(str(file_name))

                    # 同一个文件只输出一次
                    break

                # 保存文件名、行号等前缀
                prefixes = []

                # 多文件搜索时添加文件名
                if multiple_files:
                    prefixes.append(str(file_name))

                # -n：添加行号
                if "-n" in flag_set:
                    prefixes.append(str(line_number))

                # 拼接输出结果
                if prefixes:
                    result_line = ":".join(prefixes) + ":" + line
                else:
                    result_line = line

                results.append(result_line)

    # 没有任何匹配结果时，返回空字符串
    if not results:
        return ""

    # 每条结果后面都保留换行符
    return "\n".join(results) + "\n"