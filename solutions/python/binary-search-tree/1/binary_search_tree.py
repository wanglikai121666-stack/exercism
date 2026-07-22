class TreeNode:
    """二叉搜索树中的单个节点。"""

    def __init__(self, data, left=None, right=None):
        # 当前节点保存的数字。
        self.data = data

        # 左孩子：
        # 保存小于或等于当前节点 data 的子树。
        #
        # 初始时没有左孩子，所以通常是 None。
        self.left = left

        # 右孩子：
        # 保存大于当前节点 data 的子树。
        #
        # 初始时没有右孩子，所以通常是 None。
        self.right = right

    def __str__(self):
        # 方便调试时打印节点内容。
        return (
            f"TreeNode(data={self.data}, "
            f"left={self.left}, right={self.right})"
        )


class BinarySearchTree:
    """一个二叉搜索树。

    规则：

    左子树所有数字 <= 当前节点数字
    右子树所有数字 > 当前节点数字
    """

    def __init__(self, tree_data):
        # root 保存整棵树的入口，也就是根节点。
        #
        # 空列表暂时没有根节点。
        self.root = None

        # 按输入顺序把每个数字逐个插入树中。
        #
        # 第一个数字会成为根节点；
        # 后续数字会从根节点开始一路比较、一路向下。
        for value in tree_data:
            self._insert(value)

    def _insert(self, value):
        """将一个数字插入正确的位置。"""

        # 如果树目前为空，
        # 当前数字就是第一个数字，因此直接创建根节点。
        if self.root is None:
            self.root = TreeNode(value)
            return

        # 从整棵树的根节点开始寻找插入位置。
        self._insert_into_node(self.root, value)

    def _insert_into_node(self, current_node, value):
        """从 current_node 开始，递归寻找 value 的插入位置。"""

        # 如果新数字小于或等于当前节点，
        # 它应该被放在当前节点的左子树。
        if value <= current_node.data:
            # 如果左边为空，说明已经找到合适的父节点。
            #
            # 直接在这里创建新叶子节点。
            if current_node.left is None:
                current_node.left = TreeNode(value)

            else:
                # 左边已经有节点，继续进入左子树比较。
                self._insert_into_node(current_node.left, value)

        # 如果新数字大于当前节点，
        # 它应该被放在当前节点的右子树。
        else:
            # 如果右边为空，说明已经找到合适的父节点。
            #
            # 直接在这里创建新叶子节点。
            if current_node.right is None:
                current_node.right = TreeNode(value)

            else:
                # 右边已经有节点，继续进入右子树比较。
                self._insert_into_node(current_node.right, value)

    def data(self):
        """返回根节点的数据。"""

        # 根节点就是输入列表最先插入的那个数字。
        return self.root

    def sorted_data(self):
        """使用中序遍历，返回从小到大的所有数字。"""

        # result 用来收集遍历结果。
        result = []

        def in_order_traverse(current_node):
            """对当前节点及其子树做中序遍历。"""

            # 如果当前方向没有节点，递归停止。
            #
            # 例如走到叶子节点的左边或右边时，
            # current_node 就会是 None。
            if current_node is None:
                return

            # 第一步：先处理左子树。
            #
            # 左子树中的所有数字都 <= 当前节点。
            in_order_traverse(current_node.left)

            # 第二步：记录当前节点。
            result.append(current_node.data)

            # 第三步：处理右子树。
            #
            # 右子树中的所有数字都 > 当前节点。
            in_order_traverse(current_node.right)

        # 从整棵树的根节点开始中序遍历。
        in_order_traverse(self.root)

        # 因为中序遍历顺序固定为：
        # 左子树 → 当前节点 → 右子树，
        # 所以 result 天然是升序列表。
        return result