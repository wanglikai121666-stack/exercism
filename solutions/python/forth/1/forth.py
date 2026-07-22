class StackUnderflowError(Exception):
    """当某个操作需要的栈元素数量不足时抛出。"""

    pass


def evaluate(input_data):
    """执行一组简化版 Forth 指令，并返回最终栈内容。

    Args:
        input_data (list[str]): 多行 Forth 输入。

    Returns:
        list[int]: 执行完成后的栈。
    """

    # stack 是 Forth 的核心。
    #
    # 约定列表的右侧是栈顶：
    #
    # [1, 2, 3]
    #         ↑
    #        栈顶
    stack = []

    # definitions 保存用户自定义的单词。
    #
    # 例如：
    # : square DUP * ;
    #
    # 会保存为：
    # definitions["square"] = ["dup", "*"]
    definitions = {}

    # 内置操作集合。
    #
    # 后面定义自定义单词时，需要用它检查定义内容是否合法。
    built_in_words = {
        "+",
        "-",
        "*",
        "/",
        "dup",
        "drop",
        "swap",
        "over",
    }

    # 将所有输入行合并并按空格拆成 token。
    #
    # 例如：
    # ["1 2 +", "3 *"]
    #
    # 会变成：
    # ["1", "2", "+", "3", "*"]
    tokens = " ".join(input_data).lower().split()

    def is_number(token):
        """判断 token 是否可以被当作整数。"""

        try:
            int(token)
            return True
        except ValueError:
            return False

    def require_stack_items(count):
        """检查栈中是否至少有 count 个数字。"""

        if len(stack) < count:
            raise StackUnderflowError(
                "Insufficient number of items in stack"
            )

    def divide(left, right):
        """执行向 0 截断的整数除法。"""

        # 除数为 0 时，按照题目要求抛出 ZeroDivisionError。
        if right == 0:
            raise ZeroDivisionError("divide by zero")

        # Python 的 // 对负数会向下取整，
        # 但 Forth 这里需要向 0 截断。
        #
        # 例如：
        # -3 / 2 应该得到 -1，而不是 -2。
        result = abs(left) // abs(right)

        # 如果左右数字一正一负，结果应该是负数。
        if (left < 0) != (right < 0):
            result = -result

        return result

    def execute_token(token):
        """执行一个数字、内置操作或自定义单词。"""

        # 如果 token 是自定义单词，
        # 就取出它对应的定义并依次执行。
        #
        # 例如：
        # token == "square"
        # definitions["square"] == ["dup", "*"]
        if token in definitions:
            for defined_token in definitions[token]:
                execute_token(defined_token)
            return

        # 如果 token 是整数，直接压入栈顶。
        if is_number(token):
            stack.append(int(token))
            return

        # 四则运算都需要至少两个数字。
        if token in {"+", "-", "*", "/"}:
            require_stack_items(2)

            # 最后压入栈的数字，先被取出。
            #
            # 对于：
            # 10 3 -
            #
            # right == 3
            # left == 10
            right = stack.pop()
            left = stack.pop()

            # 根据不同运算符计算结果。
            if token == "+":
                result = left + right

            elif token == "-":
                result = left - right

            elif token == "*":
                result = left * right

            else:
                result = divide(left, right)

            # 将计算结果压回栈顶。
            stack.append(result)
            return

        # DUP：复制栈顶元素。
        if token == "dup":
            require_stack_items(1)
            stack.append(stack[-1])
            return

        # DROP：删除栈顶元素。
        if token == "drop":
            require_stack_items(1)
            stack.pop()
            return

        # SWAP：交换栈顶两个元素。
        if token == "swap":
            require_stack_items(2)

            # 例如：
            # [1, 2, 3] -> [1, 3, 2]
            stack[-1], stack[-2] = stack[-2], stack[-1]
            return

        # OVER：复制倒数第二个元素到栈顶。
        if token == "over":
            require_stack_items(2)

            # 例如：
            # [1, 2, 3] -> [1, 2, 3, 2]
            stack.append(stack[-2])
            return

        # 既不是数字，也不是已定义或内置操作，
        # 就属于未定义操作。
        raise ValueError("undefined operation")

    # 使用 index 手动读取 token，
    # 因为定义语法 : name ... ; 需要一次读取多个 token。
    index = 0

    while index < len(tokens):
        token = tokens[index]

        # 冒号表示开始定义一个自定义单词。
        if token == ":":
            # : 后面必须至少有一个单词名称。
            if index + 1 >= len(tokens):
                raise ValueError("undefined operation")

            # 读取并保存自定义单词名称。
            word_name = tokens[index + 1]

            # 数字不能被重新定义成单词。
            #
            # 例如：
            # : 1 2 ;
            #
            # 是非法定义。
            if is_number(word_name):
    # 数字不能作为自定义单词名称。
    #
    # 例如：
    # : 1 2 ;
    #
    # 测试要求抛出这个准确消息。
                raise ValueError("illegal operation")

            # 从单词名称后面开始读取定义内容。
            index += 2
            definition = []

            # 一直读取到分号 ;，表示定义结束。
            while index < len(tokens) and tokens[index] != ";":
                definition_token = tokens[index]

                # 在定义时，引用一个已经存在的自定义单词，
                # 就把它当前的定义展开保存。
                #
                # 这样以后原单词被重定义，
                # 当前这个单词仍保持定义当时的含义。
                if definition_token in definitions:
                    definition.extend(definitions[definition_token])

                # 数字和内置操作可以直接保存。
                elif (
                    is_number(definition_token)
                    or definition_token in built_in_words
                ):
                    definition.append(definition_token)

                # 定义内容中出现未知单词时，无法执行。
                else:
                    raise ValueError("undefined operation")

                index += 1

            # 没有找到结束分号 ;，说明定义不完整。
            if index >= len(tokens):
                raise ValueError("undefined operation")

            # 将新定义保存进字典。
            #
            # 例如：
            # : square dup * ;
            #
            # definitions["square"] = ["dup", "*"]
            definitions[word_name] = definition

        else:
            # 普通 token 按照数字、操作或自定义单词执行。
            execute_token(token)

        # 如果刚刚处理的是定义，
        # index 此时指向结束符号 ;。
        #
        # 如果刚刚处理的是普通 token，
        # index 指向当前 token。
        #
        # 加 1 后，进入下一个 token。
        index += 1

    # 返回最终栈。
    return stack