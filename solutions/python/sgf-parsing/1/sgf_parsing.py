class SgfTree:
    """
    SGF 树的节点类（题目自带，不需要修改）。
    
    每个节点有一个 properties 字典和一个 children 列表。
    properties: {属性名: [值列表]}
        注意值是列表，因为同一个属性可以有多个值，如 AB[aa][ab][ba]
    children: [SgfTree子节点]
        子节点包括"续接节点"（; 开头的）和"变体"（(...) 开头的）
    """
    def __init__(self, properties=None, children=None):
        self.properties = properties or {}
        self.children = children or []

    def __eq__(self, other):
        if not isinstance(other, SgfTree):
            return False
        for key, value in self.properties.items():
            if key not in other.properties:
                return False
            if other.properties[key] != value:
                return False
        for key in other.properties.keys():
            if key not in self.properties:
                return False
        if len(self.children) != len(other.children):
            return False
        for child, other_child in zip(self.children, other.children):
            if child != other_child:
                return False
        return True

    def __ne__(self, other):
        return not self == other


def parse(input_string):
    """
    解析 SGF 格式字符串，返回 SgfTree 对象。

    参数:
      input_string: SGF 格式的字符串

    返回值:
      SgfTree 对象

    异常:
      ValueError("tree missing")          — 空输入或格式不合法
      ValueError("tree with no nodes")   — () 中没有 ; 节点
      ValueError("property must be in uppercase") — 属性名不是大写
      ValueError("properties without delimiter")  — 属性没有 [值]
    """
    # ========== 格式校验 ==========
    if not input_string:
        raise ValueError("tree missing")

    if input_string[0] != '(':
        raise ValueError("tree missing")

    # 递归解析整棵树，pos 从 1 开始（跳过开头的 '('）
    root, pos = _parse_tree(input_string, 1)

    # 解析完后必须刚好到字符串末尾
    # 比如 "(;FF[4]" 这种缺了结尾的也算 tree missing
    if pos != len(input_string):
        raise ValueError("tree missing")

    return root


def _parse_tree(s, pos):
    """
    递归解析一棵"子树"（从 '(' 之后到对应的 ')'）。
    
    SGF 中一棵树的语法是：
        树 = "(" 序列 { 子树 } ")"
    其中：
        序列 = 节点 { 节点 }           （主走法，连续用 ; 连接）
        子树 = "(" 序列 { 子树 } ")"  （变体走法，寄存在前一个节点下）
        节点 = ";" { 属性 }

    pos: 当前解析位置，s[pos] 应该是某个字符

    返回值: (根节点, 解析结束位置)
    """
    # ---------- 第一个字符必须是 ';'（开始一个节点）----------
    # 如果 pos 越界或不是 ';'，说明没有节点
    # 例如 "()" 中，pos 指向 ')'，不符合规则 → tree with no nodes
    if pos >= len(s):
        raise ValueError("tree missing")

    if s[pos] != ';':
        raise ValueError("tree with no nodes")

    # ---------- 主循环 ----------
    # 当前层的根节点（第一个 ; 节点）
    root = None
    # 主序列的最后一个节点（; 续接时追加到这里）
    current = None

    while pos < len(s):
        c = s[pos]

        if c == ';':
            # 分号 = 开始一个新节点
            # 这是主序列的续接，还是初始节点，由 root 是否为空决定
            node, pos = _parse_node(s, pos)

            if root is None:
                # 第一个节点 → 设为根
                root = node
                current = node
            else:
                # 后续节点 → 作为前一个节点的子节点接上
                current.children.append(node)
                # current 移到新节点（方便继续续接）
                current = node

        elif c == '(':
            # 左括号 = 开始一个变体子树
            # 变体是前一个节点的"另一条分支"
            #
            # 例如 (;FF[4](;B[aa];W[ab])(;B[dd];W[ee]))
            #      在 FF 后面有两个变体，它们都是 FF 的子节点
            #
            # 注意：变体是挂在 current（最后一个 ; 节点）上
            # current 不变，这样变体之后还能续接 ; 节点
            child, pos = _parse_tree(s, pos + 1)
            current.children.append(child)
            # current 保持不变 —— 变体不影响主序列

        elif c == ')':
            # 右括号 = 当前树结束
            # pos+1 跳过 ')'，返回到上一层
            return root, pos + 1

        else:
            # 除了 ; ( ) 之外的字符在树级别是不合法的
            # 注意：属性内的 [] 及其内容已经在 _parse_node 里处理了
            raise ValueError("tree missing")

    # 循环结束没遇到 ')' → 字符串被截断了
    raise ValueError("tree missing")


def _parse_node(s, pos):
    """
    解析一个节点。
    
    节点语法：";" { 属性 }
    属性语法：KEY { "[" 值 "]" }

    KEY 必须全部大写字母
    值可以是任意字符，用 [] 包裹

    pos: 当前位置，s[pos] 应该是 ';'

    返回值: (SgfTree节点, 解析结束位置)
    """
    # pos 指向 ';'，跳过它
    pos += 1

    node = SgfTree()

    # ---------- 解析属性 ----------
    # 循环条件：当前字符不是 ; ( ) 之一
    # 因为遇到这些字符就意味着当前节点解析完毕
    while pos < len(s) and s[pos] not in (';', '(', ')'):
        # --- 检查当前字符是否能作为属性名的开头 ---
        # 如果当前位置不是大写字母，有几种可能：
        #   a) 是小写字母开头（如 `(;ff[1])` → 报错"小写"）
        #   b) 是非法符号（如 `[`、` ` 等 → 报错"无定界符"）
        if not s[pos].isupper():
            if pos < len(s) and s[pos].isalpha() and s[pos].islower():
                raise ValueError("property must be in uppercase")
            else:
                raise ValueError("properties without delimiter")

        # --- 解析属性名 (KEY) ---
        # KEY 由一个或多个大写字母组成
        key_start = pos
        while pos < len(s) and s[pos].isupper():
            pos += 1

        key = s[key_start:pos]

        # --- 检查 KEY 后面是否有小写字母混入 ---
        # 关键！如 `(;Aa[b])`，读到 key="A" 后 pos 停在 'a' 上
        # 此时必须检查下一个字符；如果是小写字母，说明属性名混入了小写
        if pos < len(s) and s[pos].isalpha() and s[pos].islower():
            raise ValueError("property must be in uppercase")

        # --- 解析属性值 ---
        # 一个属性可以有多个值：KEY[值1][值2][值3]
        values = []

        # 连续处理多个 [值]
        while pos < len(s) and s[pos] == '[':
            # 跳过 '['
            pos += 1

            # 读取值内容，直到遇到 ']'
            # 注意值内部的转义和空白字符处理
            val_chars = []
            while pos < len(s) and s[pos] != ']':
                ch = s[pos]

                # ----- 转义处理 -----
                # SGF 转义规则（针对 Text 类型）：
                # 1. \ + 换行 → 换行被删除
                # 2. \ + 其他空白字符（空格、tab 等）→ 遵循空白字符规则 → 变成空格
                # 3. \ + 非空白字符 → 该字符直接插入（不变）
                # 注意 SGF 没有 \t、\n 这样的标准转义序列
                if ch == '\\':
                    if pos + 1 < len(s):
                        next_ch = s[pos + 1]
                        if next_ch == '\n':
                            # \ 后跟换行 → 删掉换行（行继续符）
                            pos += 2
                            continue
                        elif next_ch in ' \t\v\f\r':
                            # \ 后跟其他空白字符 → 遵循空白规则 → 变空格
                            val_chars.append(' ')
                            pos += 2
                            continue
                        else:
                            # \ 后跟非空白字符 → 该字符直接插入
                            val_chars.append(next_ch)
                            pos += 2
                            continue
                    else:
                        # 字符串结尾的 \ → 保留
                        val_chars.append('\\')
                        pos += 1

                # ----- 换行处理 -----
                # 普通的换行（前面没有 \）→ 保留为换行
                elif ch == '\n':
                    val_chars.append('\n')
                    pos += 1

                # ----- 空白字符处理（非换行） -----
                # 空格、制表符等 → 全部转换为普通空格
                elif ch in ' \t\v\f\r':
                    val_chars.append(' ')
                    pos += 1

                # ----- 普通字符直接追加 -----
                else:
                    val_chars.append(ch)
                    pos += 1

            # 检查是否到了字符串末尾还没遇到 ]
            if pos >= len(s) or s[pos] != ']':
                raise ValueError("properties without delimiter")

            # 跳过 ']'
            pos += 1

            # 将值组装成字符串加入列表
            values.append(''.join(val_chars))

        # 如果没有任何 [值]，说明属性不完整
        # 例如 (;FF) 有属性名 FF 但没有值 → 报错
        if not values:
            raise ValueError("properties without delimiter")

        # 存入节点属性字典
        # 注意值是列表（因为同一个 key 可以有多个值）
        node.properties[key] = values

    return node, pos
