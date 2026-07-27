class Zipper:
    def __init__(self, focus, path):
        """
        创建一个 Zipper。

        输入：
            focus: 当前焦点所在的树（一个节点字典，或 None）
            path: 从根节点走到当前 focus 的路线记录列表

        输出：
            一个 Zipper 对象

        例子：
            Zipper({"value": 1, "left": None, "right": None}, [])
        """
        self.focus = focus
        self.path = path

    @staticmethod
    def from_tree(tree):
        """
        从一棵完整的树创建 Zipper。

        输入：
            tree: 一棵二叉树的根节点

        输出：
            一个新的 Zipper；焦点初始放在根节点

        例子：
            tree = {"value": 1, "left": None, "right": None}
            zipper = Zipper.from_tree(tree)

            zipper.value()  # 1
        """
        return Zipper(tree, [])

    def value(self):
        """
        读取当前焦点节点的值。

        输入：
            无

        输出：
            当前 focus 的 "value"

        例子：
            zipper.focus == {"value": 5, "left": None, "right": None}

            zipper.value()  # 5
        """
        return self.focus["value"]

    def set_value(self, value):
        """
        替换当前焦点节点的值，焦点位置不移动。

        输入：
            value: 新值

        输出：
            一个新的 Zipper。
            新焦点的 value 已更新，左右子树保持不变。

        例子：
            当前焦点：
                {"value": 5, "left": left_tree, "right": right_tree}

            zipper.set_value(99).focus：
                {"value": 99, "left": left_tree, "right": right_tree}
        """
        # 不直接改 self.focus。
        # 这样旧 zipper 仍然能保持原来的树结构。
        new_focus = {
            "value": value,
            "left": self.focus["left"],
            "right": self.focus["right"],
        }

        # path 不变，因为焦点仍在同一个位置。
        return Zipper(new_focus, self.path)

    def left(self):
        """
        将焦点移动到当前节点的左孩子。

        输入：
            无

        输出：
            - 有左孩子：返回新的 Zipper，focus 是左子树
            - 没有左孩子：返回 None

        例子：
                   10
                  /  \
                 5   15

            焦点在 10 时调用 left()：

            新焦点在 5。
            path 记录：
            - 父节点值是 10
            - 当前节点原来在左边
            - 父节点右子树是 15
        """
        left_tree = self.focus["left"]

        # 左子树不存在，无法继续向左移动。
        if left_tree is None:
            return None

        # 保存“以后回到父节点所需的信息”。
        crumb = {
            "parent_value": self.focus["value"],
            "direction": "left",
            "other_subtree": self.focus["right"],
        }

        # 新路径 = 原路径加上一条新的路线记录。
        new_path = self.path + [crumb]

        # 焦点移动到左子树。
        return Zipper(left_tree, new_path)

    def set_left(self, tree):
        """
        替换当前焦点节点的左子树，焦点位置不移动。

        输入：
            tree: 新的左子树；可以是节点字典，也可以是 None

        输出：
            一个新的 Zipper

        例子：
            当前焦点：
                {"value": 10, "left": {"value": 5, ...}, "right": {"value": 15, ...}}

            zipper.set_left(None).focus：
                {"value": 10, "left": None, "right": {"value": 15, ...}}
        """
        new_focus = {
            "value": self.focus["value"],
            "left": tree,
            "right": self.focus["right"],
        }

        return Zipper(new_focus, self.path)

    def right(self):
        """
        将焦点移动到当前节点的右孩子。

        输入：
            无

        输出：
            - 有右孩子：返回新的 Zipper，focus 是右子树
            - 没有右孩子：返回 None

        例子：
                   10
                  /  \
                 5   15

            焦点在 10 时调用 right()：

            新焦点在 15。
            path 记录：
            - 父节点值是 10
            - 当前节点原来在右边
            - 父节点左子树是 5
        """
        right_tree = self.focus["right"]

        # 右子树不存在，无法继续向右移动。
        if right_tree is None:
            return None

        crumb = {
            "parent_value": self.focus["value"],
            "direction": "right",
            "other_subtree": self.focus["left"],
        }

        new_path = self.path + [crumb]

        # 焦点移动到右子树。
        return Zipper(right_tree, new_path)

    def set_right(self, tree):
        """
        替换当前焦点节点的右子树，焦点位置不移动。

        输入：
            tree: 新的右子树；可以是节点字典，也可以是 None

        输出：
            一个新的 Zipper

        例子：
            当前焦点：
                {"value": 10, "left": {"value": 5, ...}, "right": {"value": 15, ...}}

            zipper.set_right(None).focus：
                {"value": 10, "left": {"value": 5, ...}, "right": None}
        """
        new_focus = {
            "value": self.focus["value"],
            "left": self.focus["left"],
            "right": tree,
        }

        return Zipper(new_focus, self.path)

    def up(self):
        """
        将焦点移动回父节点。

        输入：
            无

        输出：
            - 当前不是根节点：返回新的 Zipper，focus 是重新拼好的父节点
            - 当前已经是根节点：返回 None

        例子：
            原树：
                   10
                  /  \
                 5   15

            焦点从 10 向左移动后，focus 是 5。

            此时调用 up()，根据 path 中的记录拼回：

                   10
                  /  \
                 5   15

            焦点重新回到 10。
        """
        # path 为空，说明当前 focus 已经是根节点。
        if not self.path:
            return None

        # 最后一条路线记录，就是当前节点的父节点信息。
        crumb = self.path[-1]

        # 回到父节点后，最末尾的路线记录不再需要。
        new_path = self.path[:-1]

        # 如果当前 focus 原来是父节点的左孩子，
        # 那么“当前 focus”放回 left；
        # 保存的 other_subtree 放回 right。
        if crumb["direction"] == "left":
            parent = {
                "value": crumb["parent_value"],
                "left": self.focus,
                "right": crumb["other_subtree"],
            }

        # 如果当前 focus 原来是父节点的右孩子，
        # 保存的 other_subtree 放回 left；
        # 当前 focus 放回 right。
        else:
            parent = {
                "value": crumb["parent_value"],
                "left": crumb["other_subtree"],
                "right": self.focus,
            }

        return Zipper(parent, new_path)

    def to_tree(self):
        """
        从当前焦点一路向上拼回去，获得完整二叉树。

        输入：
            无

        输出：
            完整二叉树的根节点字典

        例子：
            原树：
                   10
                  /  \
                 5   15

            zipper = Zipper.from_tree(tree).left().set_value(99)

            zipper.to_tree() 返回：
            {
                "value": 10,
                "left": {"value": 99, "left": None, "right": None},
                "right": {"value": 15, "left": None, "right": None},
            }
        """
        current_zipper = self

        # 不断向上，直到 up() 返回 None，也就是到达根节点。
        while True:
            parent_zipper = current_zipper.up()

            if parent_zipper is None:
                # 此时 focus 已经是拼好的整棵树。
                return current_zipper.focus

            current_zipper = parent_zipper