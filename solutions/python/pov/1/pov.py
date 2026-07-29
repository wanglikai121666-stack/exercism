from json import dumps


class Tree:
    def __init__(self, label, children=None):
        # 节点名称
        self.label = label

        # 子节点列表；没有传入时默认为空列表
        self.children = children if children is not None else []

    def __dict__(self):
        """
        将树转换成字典，供测试比较。

        例如：
        Tree("a", [Tree("b")])

        返回：
        {"a": [{"b": []}]}
        """
        return {
            self.label: [
                child.__dict__()
                for child in sorted(self.children)
            ]
        }

    def __str__(self, indent=None):
        """将树转换为 JSON 格式字符串。"""
        return dumps(self.__dict__(), indent=indent)

    def __lt__(self, other):
        """使 Tree 对象可以根据 label 排序。"""
        return self.label < other.label

    def __eq__(self, other):
        """判断两棵树结构是否相同。"""
        return self.__dict__() == other.__dict__()

    def _build_graph(self, parent=None, graph=None):
        """
        将树转成无方向图（双向连接）。

        原 Tree：
            0
            |
            2
            |
            6

        转换后 graph：
        {
            0: [2],
            2: [0, 6],
            6: [2]
        }
        """
        if graph is None:
            graph = {}

        # 当前节点没有出现过，就创建邻居列表
        if self.label not in graph:
            graph[self.label] = []

        # 父节点和当前节点建立双向连接
        if parent is not None:
            graph[self.label].append(parent)
            graph[parent].append(self.label)

        # 递归处理每一个子节点
        for child in self.children:
            child._build_graph(self.label, graph)

        return graph

    def _make_tree(self, label, graph, parent=None):
        """
        从指定 label 开始，根据双向图重新生成 Tree。

        parent 用于避免又走回父节点造成无限递归。
        """
        children = []

        for neighbor in graph[label]:
            # 如果 neighbor 是刚刚走来的父节点，就跳过
            if neighbor != parent:
                children.append(
                    self._make_tree(neighbor, graph, label)
                )

        return Tree(label, children)

    def from_pov(self, from_node):
        """
        以 from_node 为新根，返回重新定根后的树。
        """
        # 先把原树转换成双向连接图
        graph = self._build_graph()

        # 新根不存在，无法重建树
        if from_node not in graph:
            raise ValueError("Tree could not be reoriented")

        # 从新根开始生成新的树
        return self._make_tree(from_node, graph)

    def path_to(self, from_node, to_node):
        """
        返回从 from_node 到 to_node 的节点路径。

        例如：
        [6, 2, 0, 3, 9]
        """
        graph = self._build_graph()

        # 起点不存在：无法以它为视角重新定根
        if from_node not in graph:
            raise ValueError("Tree could not be reoriented")

        # 终点不存在：无法找到路径
        if to_node not in graph:
            raise ValueError("No path found")

        def find_path(current, target, visited):
            """
            从 current 开始寻找 target。
            找到时返回路径列表；找不到时返回 None。
            """
            # 到达终点
            if current == target:
                return [current]

            # 记录已访问节点，避免重复访问
            visited.add(current)

            # 遍历所有相邻节点
            for neighbor in graph[current]:
                if neighbor not in visited:
                    result = find_path(neighbor, target, visited)

                    # 找到终点时，当前节点加到路径最前面
                    if result is not None:
                        return [current] + result

            return None

        path = find_path(from_node, to_node, set())

        # 正常的树中，只要两个节点都存在，一定有路径；
        # 这里仍保留异常处理，以符合题目要求。
        if path is None:
            raise ValueError("No path found")

        return path