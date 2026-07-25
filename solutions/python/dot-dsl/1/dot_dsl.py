NODE, EDGE, ATTR = range(3)


class Node:
    def __init__(self, name, attrs):
        # 节点自己的名字，例如 "a"
        self.name = name

        # 节点的属性字典，例如 {"color": "red"}
        self.attrs = attrs

    def __eq__(self, other):
        # 让测试可以直接比较两个 Node 对象的内容
        return self.name == other.name and self.attrs == other.attrs


class Edge:
    def __init__(self, src, dst, attrs):
        # 边从哪个节点出发，例如 "a"
        self.src = src

        # 边连接到哪个节点，例如 "b"
        self.dst = dst

        # 边的属性字典，例如 {"color": "green"}
        self.attrs = attrs

    def __eq__(self, other):
        # 让测试可以直接比较两个 Edge 对象的内容
        return (
            self.src == other.src
            and self.dst == other.dst
            and self.attrs == other.attrs
        )


class Graph:
    def __init__(self, data=None):
        # 没有传数据时，创建一张空图
        if data is None:
            data = []

        # 整体必须是一张“声明列表”
        # 例如 [(NODE, "a", {}), (EDGE, "a", "b", {})]
        if not isinstance(data, list):
            raise TypeError("Graph data malformed")

        # Graph 最终内部保存的三种数据
        self.nodes = []
        self.edges = []
        self.attrs = {}

        # 逐条读取图的声明
        for item in data:
            # 每一条声明必须至少是一个有两个位置的 tuple。
            # 第一个位置表示类型，后面至少还应有内容。
            if not isinstance(item, tuple) or len(item) < 2:
                raise TypeError("Graph item incomplete")

            item_type = item[0]

            # 图属性：
            # (ATTR, "bgcolor", "yellow")
            if item_type == ATTR:
                # 属性声明必须刚好有 3 个值
                if len(item) != 3:
                    raise ValueError("Attribute is malformed")

                key = item[1]
                value = item[2]

                # 保存为字典：{"bgcolor": "yellow"}
                self.attrs[key] = value

            # 节点：
            # (NODE, "a", {"color": "red"})
            elif item_type == NODE:
                # 节点必须有：类型、名字、属性字典
                if len(item) != 3:
                    raise ValueError("Node is malformed")

                name = item[1]
                attrs = item[2]

                # 创建 Node 对象，并加入节点列表
                self.nodes.append(Node(name, attrs))

            # 边：
            # (EDGE, "a", "b", {"color": "green"})
            elif item_type == EDGE:
                # 边必须有：类型、起点、终点、属性字典
                if len(item) != 4:
                    raise ValueError("Edge is malformed")

                src = item[1]
                dst = item[2]
                attrs = item[3]

                # 创建 Edge 对象，并加入边列表
                self.edges.append(Edge(src, dst, attrs))

            # 第一个位置既不是 ATTR、NODE、EDGE，就不认识
            else:
                raise ValueError("Unknown item")