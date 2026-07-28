def tree_from_traversals(preorder, inorder):
    """
    从前序遍历和中序遍历序列构造二叉树（Codewars 字典表示法）。

    ────────────────────────────────────────────────────────────
    题目翻译：
      给你两个列表：
        preorder（前序遍历，顺序是 根→左→右）
        inorder（中序遍历，顺序是 左→根→右）
      请你还原出这棵二叉树，返回它的根节点（用字典表示）。

    ────────────────────────────────────────────────────────────
    字典表示法约定（Codewars 平台）：
      空树            = {}                                      (空字典)
      单个节点         = {"v": value, "l": left, "r": right}
        其中 v = value（节点值）
             l = left（左子树，本身也是个字典或 {}）
             r = right（右子树，本身也是个字典或 {}）

    例子：
        pre = [3, 9, 20, 15, 7]
        ino = [9, 3, 15, 20, 7]
      还原出的树是：
             3
            / \
           9  20
             /  \
            15   7
      对应的字典表示：
        {"v": 3, "l": {"v": 9, "l": {}, "r": {}},
                   "r": {"v": 20, "l": {"v": 15, "l": {}, "r": {}},
                                 "r": {"v": 7, "l": {}, "r": {}}}}

    ────────────────────────────────────────────────────────────
    核心口诀（三轮是一样的套路）：
      前序定根 → 中序定界 → 长度切前序 → 递归

    具体做法（每轮都重复这 4 步）：
      ① 前序第一个元素 = 当前树的根
      ② 拿根去中序里找位置 → 根左边全是左子树，右边全是右子树
      ③ 数左子树有几个节点 → 回前序里把根后面同样多个切出来给左子树
         剩下的给右子树
      ④ 左右子树各自拿到一对(前序, 中序) → 递归做同样的事

    ────────────────────────────────────────────────────────────
    三轮展开（以 pre=[a,b,d,e,c,f,g], in=[d,b,e,a,f,c,g] 为例）：

    第 1 轮：整棵树
      pre[0]=a → 根=a
      在 in 里找 a，它在索引 3 → 左子树=[d,b,e](3个)  右子树=[f,c,g](3个)
      去 pre 里切：a 后面 3 个 [b,d,e] 给左子树，剩下 [c,f,g] 给右子树
      递归 → tree_from_traversals([b,d,e], [d,b,e])   # 左子树
             tree_from_traversals([c,f,g], [f,c,g])   # 右子树

    第 2 轮：
      [左子树] pre=[b,d,e] in=[d,b,e]
        pre[0]=b, in 中 b 在索引 1 → 左[d] 右[e]
        切前序：b 后 1 个 [d] 左，剩下 [e] 右
        递归 → tree_from_traversals([d],[d])    # 左左 → 返回 {"v":d, "l":{}, "r":{}}
               tree_from_traversals([e],[e])    # 左右 → 返回 {"v":e, "l":{}, "r":{}}
      [右子树] pre=[c,f,g] in=[f,c,g]
        pre[0]=c, in 中 c 在索引 1 → 左[f] 右[g]
        递归 → tree_from_traversals([f],[f])    # 右左 → 返回 {"v":f, "l":{}, "r":{}}
               tree_from_traversals([g],[g])    # 右右 → 返回 {"v":g, "l":{}, "r":{}}

    第 3 轮：
      pre=[d] in=[d] → pre[0]=d, in 中 d 在索引 0 → 左[] 右[]
        左子树 = tree_from_traversals([], []) = {}    # 空树
        右子树 = tree_from_traversals([], []) = {}    # 空树
        返回 {"v": d, "l": {}, "r": {}}
      同理 e, f, g。
      递归回退时，每层把左右子树包到 v/l/r 里，逐层拼回整棵树。
    ────────────────────────────────────────────────────────────
    """
    # ========== 输入校验（Codewars Test 4~6 要求的）==========
    # ① 两个列表长度必须相等
    #    测试例：preorder=["a","b"], inorder=["b","a","r"] → 长度 2 ≠ 3
    #    这种情况根本无法构造出合法的树，所以要主动抛错
    if len(preorder) != len(inorder):
        raise ValueError("traversals must have the same length")

    # ② 长度相同，但内容（元素集合）必须一致
    #    测试例：preorder=["a","b"], inorder=["c","d"] → 长度都是 2，但元素不同
    #    用 sorted 排序后逐位比较，可以处理任意顺序
    if sorted(preorder) != sorted(inorder):
        raise ValueError("traversals must have the same elements")

    # ③ 元素必须唯一，不能有重复
    #    测试例：preorder=["a","b","a"], inorder=["b","a","a"] → a 出现了两次
    #    把 list 转成 set 后长度会变小（重复的被去重），所以看长度是否变化
    if len(set(preorder)) != len(preorder):
        raise ValueError("traversals must contain unique items")

    # ========== 递归终止条件 ==========
    # 如果 preorder 是空列表，说明当前没有节点了
    # Codewars 平台约定：空树用空字典 {} 表示
    # 比如 pre=[d] 的左右子树 pre=[], in=[] → 直接返回 {}
    # 这个 {} 会被它的父节点接收，作为 "l" 或 "r" 的值
    if not preorder:
        return {}

    # ========== 第 ① 步：前序定根 ==========
    # 前序遍历永远先访问根节点，所以 preorder[0] 就是当前这棵树的根
    root_val = preorder[0]

    # ========== 第 ② 步：中序定界 ==========
    # 中序遍历是左→根→右，所以根节点会在中序序列的某个位置
    # 这个位置把中序切成两半：左边是左子树，右边是右子树
    #
    # 例如 in=[d,b,e,a,f,c,g]，根=a → root_index=3
    #   inorder[:3]  = [d,b,e]  → 左子树的全部节点
    #   inorder[4:]  = [f,c,g]  → 右子树的全部节点
    root_index = inorder.index(root_val)

    # ========== 第 ③ 步：切分序列 ==========
    #
    # 中序切分（直接用 root_index 切）：
    #   - root_index 左边 = 左子树的中序
    #   - root_index 右边 = 右子树的中序
    left_inorder  = inorder[:root_index]       # 例如 [d,b,e]
    right_inorder = inorder[root_index + 1:]   # 例如 [f,c,g]

    # 左子树有几个节点？
    # 这个数字就是用来切前序的"尺子"
    left_size = len(left_inorder)              # 例如 3

    # 前序切分（用 left_size 切）：
    #   - preorder[0] 已经被拿走了（根）
    #   - preorder[1 : 1+left_size] = 左子树的前序
    #   - preorder[1+left_size :]   = 右子树的前序
    #
    # 为什么能这么切？
    # 前序遍历的顺序是 根→(左子树整体)→(右子树整体)
    # 左子树中序的长度 = 左子树的节点数 = 左子树前序的长度
    # 所以知道了左子树有几个节点，就能在前序里精确切出左子树的范围
    left_preorder  = preorder[1 : 1 + left_size]     # 例如 [b,d,e]
    right_preorder = preorder[1 + left_size :]       # 例如 [c,f,g]

    # ========== 第 ④ 步：递归构造左右子树 ==========
    # 现在左子树有它自己的(前序, 中序)对：
    #   left_preorder + left_inorder
    # 右子树也有它自己的对：
    #   right_preorder + right_inorder
    #
    # 递归调用 tree_from_traversals，它们会重复做：
    #   前序定根 → 中序定界 → 长度切前序 → 递归
    # 直到 preorder 为空（返回 {}）或只剩一个元素（直接成叶节点）
    left_subtree  = tree_from_traversals(left_preorder, left_inorder)
    right_subtree = tree_from_traversals(right_preorder, right_inorder)

    # ========== 拼装当前根节点（字典表示） ==========
    # 把根值、左子树、右子树打包成 Codewars 的字典格式
    #   v = value（节点值）
    #   l = left（左子树，可能是另一个字典，也可能是空字典 {}）
    #   r = right（右子树，可能是另一个字典，也可能是空字典 {}）
    #
    # 注意：当递归到底时（叶节点），left_subtree 和 right_subtree 都是 {}
    # 这正好对应了叶节点"没有左右子树"的语义
    return {"v": root_val, "l": left_subtree, "r": right_subtree}


# ===================== 测试 =====================
if __name__ == "__main__":
    # 字典格式的遍历函数：给定一个字典表示的树，返回前序/中序列表
    def preorder_traverse(node):
        # node 为空字典 {} → 返回空列表
        if not node:
            return []
        return [node["v"]] + preorder_traverse(node["l"]) + preorder_traverse(node["r"])

    def inorder_traverse(node):
        if not node:
            return []
        return inorder_traverse(node["l"]) + [node["v"]] + inorder_traverse(node["r"])

    # 测试用例 1（之前图里用的字母例子）
    preorder = ['a', 'b', 'd', 'e', 'c', 'f', 'g']
    inorder  = ['d', 'b', 'e', 'a', 'f', 'c', 'g']
    tree = tree_from_traversals(preorder, inorder)

    print("=== 测试 1（字母例）===")
    print("前序:", preorder_traverse(tree))   # 应与 preorder 一致
    print("中序:", inorder_traverse(tree))    # 应与 inorder 一致
    print("树:", tree)
    print()

    # 测试用例 2（更常见的数字例子）
    #       3
    #      / \
    #     9  20
    #       /  \
    #      15   7
    preorder2 = [3, 9, 20, 15, 7]
    inorder2  = [9, 3, 15, 20, 7]
    tree2 = tree_from_traversals(preorder2, inorder2)

    print("=== 测试 2（数字例）===")
    print("前序:", preorder_traverse(tree2))  # 期望: [3, 9, 20, 15, 7]
    print("中序:", inorder_traverse(tree2))   # 期望: [9, 3, 15, 20, 7]
    print("树:", tree2)
    print()

    # 测试用例 3：空树（Codewars 第 1 个测试用例的格式）
    tree3 = tree_from_traversals([], [])
    print("=== 测试 3（空树）===")
    print("根节点:", tree3)              # 期望: {}
    print("是否等于 {}:", tree3 == {})    # 期望: True
    print()

    # 测试用例 4：只有根节点
    tree4 = tree_from_traversals([1], [1])
    print("=== 测试 4（单节点）===")
    print("根节点:", tree4)                # 期望: {"v":1, "l":{}, "r":{}}
    print("v:", tree4["v"])                # 期望: 1
    print("l:", tree4["l"])                # 期望: {}
    print("r:", tree4["r"])                # 期望: {}
    print()
