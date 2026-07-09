def answer(question):
    """
    解析并计算简单英文数学题。
    """

    # 题目必须是固定格式：
    # What is ...?
    if not question.startswith("What is ") or not question.endswith("?"):
        raise ValueError("syntax error")

    # 去掉开头的 "What is " 和结尾的 "?"
    # 例如：
    # "What is 5 plus 13?" -> "5 plus 13"
    expression = question[len("What is "):-1].strip()

    # 如果中间没有内容，比如 "What is ?"
    if expression == "":
        raise ValueError("syntax error")

    # 把两个词组成的操作合并成一个 token
    # 否则 split 后会被拆开
    #
    # "multiplied by" -> "multiplied_by"
    # "divided by" -> "divided_by"
    expression = expression.replace("multiplied by", "multiplied_by")
    expression = expression.replace("divided by", "divided_by")

    # 拆成 token
    # 例如：
    # "3 plus 2 multiplied_by 3"
    # -> ["3", "plus", "2", "multiplied_by", "3"]
    tokens = expression.split()

    # 第一个 token 必须是数字
    if not is_number(tokens[0]):
        raise ValueError("syntax error")

    # 第一个数字作为初始结果
    result = int(tokens[0])

    # 从第二个 token 开始，每次读取：
    # 操作符 + 下一个数字
    index = 1

    while index < len(tokens):
        operation = tokens[index]

        # 这里应该是操作符，如果又出现数字，说明语法错了
        # 例如：
        # What is 1 2?
        if is_number(operation):
            raise ValueError("syntax error")

        # 只支持这四种操作
        if operation not in ["plus", "minus", "multiplied_by", "divided_by"]:
            raise ValueError("unknown operation")

        # 操作符后面必须还有一个数字
        # 例如：
        # What is 1 plus?
        if index + 1 >= len(tokens):
            raise ValueError("syntax error")

        next_token = tokens[index + 1]

        # 操作符后面必须是数字
        # 例如：
        # What is 1 plus plus 2?
        if not is_number(next_token):
            raise ValueError("syntax error")

        number = int(next_token)

        # 从左到右计算，不管正常数学优先级
        if operation == "plus":
            result += number
        elif operation == "minus":
            result -= number
        elif operation == "multiplied_by":
            result *= number
        elif operation == "divided_by":
            result //= number

        # 这轮处理了两个 token：
        # operation 和 number
        index += 2

    return result


def is_number(token):
    """
    判断 token 能不能转成整数。

    支持：
    "5"
    "-5"

    不支持：
    "plus"
    "cubed"
    """
    try:
        int(token)
        return True
    except ValueError:
        return False