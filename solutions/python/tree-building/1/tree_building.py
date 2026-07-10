class Record:
    def __init__(self, record_id, parent_id):
        self.record_id = record_id
        self.parent_id = parent_id


class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.children = []


def BuildTree(records):
    # 空列表没有树
    if not records:
        return None

    # 按 record_id 从小到大排序
    records.sort(key=lambda record: record.record_id)

    # 检查 record_id 是否从 0 开始并连续
    for expected_id, record in enumerate(records):
        if record.record_id != expected_id:
            raise ValueError("Record id is invalid or out of order.")

    # 检查每个节点的 parent_id
    for record in records:
        # 情况一：
        # parent_id 比自己的 record_id 大，非法
        if record.parent_id > record.record_id:
            raise ValueError(
                "Node parent_id should be smaller than its record_id."
            )

        # 情况二：
        # parent_id 和 record_id 相等
        if record.parent_id == record.record_id:
            # 只有根节点 0 才允许自己指向自己
            if record.record_id != 0:
                raise ValueError(
                    "Only root should have equal record and parent id."
                )

    # 为每条记录创建对应的节点
    nodes = [Node(record.record_id) for record in records]

    # 把每个普通节点挂到对应父节点下面
    for record in records[1:]:
        parent_node = nodes[record.parent_id]
        child_node = nodes[record.record_id]

        parent_node.children.append(child_node)

    # 0 号节点是根节点
    return nodes[0]