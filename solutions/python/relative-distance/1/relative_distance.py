from collections import defaultdict, deque


class RelativeDistance:
    def __init__(self, family_tree):
        """
        把原始家谱转换成邻接表。

        neighbors中的结构是：
        {
            "某个人": {"直接相连的人1", "直接相连的人2"}
        }
        """

        # defaultdict(set)表示：
        # 如果某个人还不存在，就自动创建一个空set。
        self.neighbors = defaultdict(set)

        # family_tree格式：
        # {
        #     "父母": ["孩子1", "孩子2"]
        # }
        for parent, children in family_tree.items():
            # 即使parent没有孩子，也把他记录到家谱中。
            self.neighbors[parent]

            # 建立父母和孩子之间的双向连接。
            for child in children:
                # parent → child
                self.neighbors[parent].add(child)

                # child → parent
                self.neighbors[child].add(parent)

            # 同一个父母的孩子互为兄弟姐妹。
            # 本题规定兄弟姐妹之间的距离是1，
            # 所以需要把他们直接连接起来。
            for first_index in range(len(children)):
                for second_index in range(
                    first_index + 1,
                    len(children),
                ):
                    first_child = children[first_index]
                    second_child = children[second_index]

                    # 建立兄弟姐妹之间的双向连接。
                    self.neighbors[first_child].add(second_child)
                    self.neighbors[second_child].add(first_child)

    def degree_of_separation(self, person_a, person_b):
        """
        使用BFS计算person_a到person_b的最短距离。
        """

        # 必须先检查A是否存在。
        if person_a not in self.neighbors:
            raise ValueError("Person A not in family tree.")

        # 再检查B是否存在。
        if person_b not in self.neighbors:
            raise ValueError("Person B not in family tree.")

        # 队列中保存：
        # (当前人物, 当前人物与person_a之间的距离)
        queue = deque([
            (person_a, 0),
        ])

        # 记录已经发现的人，避免重复搜索和形成循环。
        visited = {person_a}

        while queue:
            # 取出队列最左边的人。
            current_person, distance = queue.popleft()

            # BFS第一次找到目标时，就是最短距离。
            if current_person == person_b:
                return distance

            # 查看与当前人物直接相连的所有人。
            for neighbor in self.neighbors[current_person]:
                # 已经访问过的人不再加入队列。
                if neighbor in visited:
                    continue

                # 在加入队列时就标记为已访问，
                # 避免同一个人被重复加入队列。
                visited.add(neighbor)

                # 邻居比当前人物多一层关系。
                queue.append((
                    neighbor,
                    distance + 1,
                ))

        # 队列为空仍然没有找到B，
        # 说明两个人虽然都在家谱中，但属于不同家族。
        raise ValueError(
            "No connection between person A and person B."
        )